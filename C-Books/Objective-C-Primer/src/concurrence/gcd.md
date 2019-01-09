# GCD(Grand Central Dispatch)介绍

为了让开发者更加容易的使用设备上的多核 CPU，苹果在 OS X 10.6 和 iOS 4 中引入了 **Grand Central Dispatch（GCD）**。

通过 GCD，开发者不用再直接跟线程打交道了，只需要向队列中添加代码块即可，GCD 在后端管理着一个线程池。GCD 不仅决定着你的代码块将在哪个线程被执行，它还根据可用的系统资源对这些线程进行管理。这样可以将开发者从线程管理的工作中解放出来，通过集中的管理线程，来缓解大量线程被创建的问题。

GCD 带来的另一个重要改变是，作为开发者可以将工作考虑为一个队列，而不是一堆线程，这种并行的抽象模型更容易掌握和使用。

GCD 公开有 5 个不同的队列：运行在主线程中的 main queue，3 个不同优先级的后台队列，以及一个优先级更低的后台队列（用于 I/O）。 另外，开发者可以创建自定义队列：串行或者并行队列。自定义队列非常强大，在自定义队列中被调度的所有 block 最终都将被放入到系统的全局队列中和线程池中。

![](concurrence/images/gcd_concept.png)

使用不同优先级的若干个队列乍听起来非常直接，不过，我们强烈建议，在绝大多数情况下使用默认的优先级队列就可以了。如果执行的任务需要访问一些共享的资源，那么在不同优先级的队列中调度这些任务很快就会造成不可预期的行为。这样可能会引起程序的完全挂起，因为低优先级的任务阻塞了高优先级任务，使它不能被执行。

虽然 GCD 是一个低层级的 C API ，但是它使用起来非常的直接。不过这也容易使开发者忘记并发编程中的许多注意事项和陷阱。

## 并发编程中面临的挑战

使用并发编程会带来许多陷阱。只要一旦你做的事情超过了最基本的情况，对于并发执行的多任务之间的相互影响的不同状态的监视就会变得异常困难。 问题往往发生在一些不确定性（不可预见性）的地方，这使得在调试相关并发代码时更加困难。

关于并发编程的不可预见性有一个非常有名的例子：在 1995 年， NASA (美国宇航局)发送了开拓者号火星探测器，但是当探测器成功着陆在我们红色的邻居星球后不久，任务`嘎然而止`，火星探测器莫名其妙的不停重启，在计算机领域内，遇到的这种现象被定为为`优先级反转`，也就是说低优先级的线程一直阻塞着高优先级的线程。稍后我们会看到关于这个问题的更多细节。在这里我们想说明的是，即使拥有丰富的资源和大量优秀工程师的智慧，并发也还是会在不少情况下反咬你你一口。

//TODO: 底层并发 API

## Operation Queues 操作队列

操作队列（operation queue）是由 GCD 提供的一个队列模型的 Cocoa 抽象。GCD 提供了更加底层的控制，而操作队列则在 GCD 之上实现了一些方便的功能，这些功能对于 app 的开发者来说通常是最好最安全的选择。

`NSOperationQueue` 有两种不同类型的队列：`主队列`和`自定义队列`。主队列运行在主线程之上，而自定义队列在后台执行。在两种类型中，这些队列所处理的任务都使用 `NSOperation` 的子类来表述。

你可以通过重写 `main` 或者 `start` 方法 来定义自己的 `operations` 。前一种方法非常简单，开发者不需要管理一些状态属性（例如 `isExecuting` 和 `isFinished`），当 `main` 方法返回的时候，这个 `operation` 就结束了。这种方式使用起来非常简单，但是灵活性相对重写 `start` 来说要少一些。

```cpp
@implementation YourOperation
    - (void)main
    {
        // 进行处理 ...
    }
@end
```

如果你希望拥有更多的控制权，以及在一个操作中可以执行异步任务，那么就重写 `start` 方法：

```cpp
@implementation YourOperation
    - (void)start
    {
        self.isExecuting = YES;
        self.isFinished = NO;
        // 开始处理，在结束时应该调用 finished ...
    }

    - (void)finished
    {
        self.isExecuting = NO;
        self.isFinished = YES;
    }
@end
```

注意：这种情况下，你必须手动管理操作的状态。 为了让操作队列能够捕获到操作的改变，需要将状态的属性以配合 KVO 的方式进行实现。如果你不使用它们默认的 setter 来进行设置的话，你就需要在合适的时候发送合适的 KVO 消息。

为了能使用操作队列所提供的取消功能，你需要在长时间操作中时不时地检查 `isCancelled` 属性：

```cpp
- (void)main
{
    while (notDone && !self.isCancelled) {
        // 进行处理
    }
}
```

当你定义好 operation 类之后，就可以很容易的将一个 operation 添加到队列中：

```cpp
NSOperationQueue *queue = [[NSOperationQueue alloc] init];
YourOperation *operation = [[YourOperation alloc] init];
[queue  addOperation:operation];
```

另外，你也可以将 block 添加到操作队列中。这有时候会非常的方便，比如你希望在主队列中调度一个一次性任务：

```cpp
[[NSOperationQueue mainQueue] addOperationWithBlock:^{
    // 代码...
}];
```

虽然通过这种的方式在队列中添加操作会非常方便，但是定义你自己的 `NSOperation` 子类会在调试时很有帮助。如果你重写 `operation` 的`description` 方法，就可以很容易的标示出在某个队列中当前被调度的所有操作 。

除了提供基本的调度操作或 `block` 外，操作队列还提供了在 `GCD` 中不太容易处理好的特性的功能。例如，你可以通过 `maxConcurrentOperationCount` 属性来控制一个特定队列中可以有多少个操作参与并发执行。将其设置为 1 的话，你将得到一个串行队列，这在以隔离为目的的时候会很有用。

另外还有一个方便的功能就是根据队列中 `operation` 的优先级对其进行排序，这不同于 `GCD` 的队列优先级，它只影响当前队列中所有被调度的 `operation` 的执行先后。如果你需要进一步在除了 5 个标准的优先级以外对 `operation` 的执行顺序进行控制的话，还可以在 `operation` 之间指定依赖关系，如下：

```cpp
[intermediateOperation addDependency:operation1];
[intermediateOperation addDependency:operation2];
[finishedOperation addDependency:intermediateOperation];
```

这些简单的代码可以确保 `operation1` 和 `operation2` 在 `intermediateOperation` 之前执行，当然，也会在 `finishOperation` 之前被执行。对于需要明确的执行顺序时，操作依赖是非常强大的一个机制。它可以让你创建一些操作组，并确保这些操作组在依赖它们的操作被执行之前执行，或者在并发队列中以串行的方式执行操作。

**从本质上来看，操作队列的性能比 GCD 要低那么一点，不过，大多数情况下这点负面影响可以忽略不计，操作队列是并发编程的首选工具。**

## Run Loops 与并发编程有关的循环处理

实际上，`Run loop`并不像 GCD 或者操作队列那样是一种并发机制，因为它并不能并行执行任务。不过在主 `dispatch/operation` 队列中， `run loop` 将直接配合任务的执行，它提供了一种异步执行代码的机制。

`Run loop` 比起操作队列或者 GCD 来说容易使用得多，因为通过 `run loop` ，你不必处理并发中的复杂情况，就能异步地执行任务。

一个 `run loop` 总是绑定到某个特定的线程中。`main run loop` 是与主线程相关的，在每一个 `Cocoa` 和 `CocoaTouch` 程序中，这个 `main run loop` 都扮演了一个核心角色，它负责处理 UI 事件、计时器，以及其它内核相关事件。无论你什么时候设置计时器、使用 `NSURLConnection` 或者调用 performSelector:withObject:afterDelay:，其实背后都是 run loop 在处理这些异步任务。

无论何时你使用 `run loop` 来执行一个方法的时候，都需要记住一点：`run loop` 可以运行在不同的模式中，每种模式都定义了一组事件，供 `run loop` 做出响应。这在对应 `main run loop` 中暂时性的将某个任务优先执行这种任务上是一种聪明的做法。

关于这点，在 iOS 中非常典型的一个示例就是滚动。在进行滚动时，run loop 并不是运行在默认模式中的，因此， run loop 此时并不会响应比如滚动前设置的计时器。一旦滚动停止了，run loop 会回到默认模式，并执行添加到队列中的相关事件。如果在滚动时，希望计时器能被触发，需要将其设为 `NSRunLoopCommonModes` 的模式，并添加到 run loop 中。

主线程一般来说都已经配置好了 main run loop。然而其他线程默认情况下都没有设置 run loop。你也可以自行为其他线程设置 run loop ，但是一般来说我们很少需要这么做。大多数时间使用 main run loop 会容易得多。如果你需要处理一些很重的工作，但是又不想在主线程里做，你仍然可以在你的代码在 main run loop 中被调用后将工作分配给其他队列。

**备注：**

> 如果你真需要在别的线程中添加一个 run loop ，那么不要忘记在 run loop 中至少添加一个 input source 。如果 run loop 中没有设置好的 input source，那么每次运行这个 run loop ，它都会立即退出。

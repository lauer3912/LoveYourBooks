# @selector 与 SEL 如何理解？

## 场景

异型进度条的时候用到了定时器 `NSTimer`,其中定时器的启动是这么写的：

```cpp
_timer = [NSTimer scheduledTimerWithTimeInterval:0.1
                                            target:self
                                            selector:@selector(circleAnimationTypeOne)
                                            userInfo:nil
                                            repeats:YES];
```

## 简介

- Selector 是一个对象中用来选择方法来执行的名字，或者是当源代码编译时候用来替换名字的唯一的标示。
- Selector 自己并不能做任何事情。它简单的标示了一个方法。使得 selector 方法名称不同于普通字符串的唯一的事情是编译器确定 selectors 是独特的。使得 selector 有用的是（与运行时结合）它扮演着类似于一个动态函数指针，对于一个已经给与的名字，自动指向类所使用的适用的方法的实现。假设我们有一个 run 方法的 selector，并且类 Dog，Athlete 和 ComputerSimulation（每个类都实现了 run 方法）。
- Selector 能够被每一个类的实例所使用并且调用它的 run 方法--设置方法的实现可能是互不相同的。

## 如何获得 `Selector`

被编译的 selectors 是 SEL 类型的。有两种方式获得 selector：

1. 在编译期，我们使用编译标示@selector

```cpp
SEL aSelector = @selector(methodName);
```

1. 在运行时，我们使用 NSSelectorFromString 方法，字符串是方法名：

```cpp
SEL aSelector = NSSelectorFromString(@"methodName");

// 当我们想要我们的代码发送一个知道运行时我们才知道名字的消息的时候，我们使用selector创建一个字符串。
```

## 如何使用 `Selector`

能够调用以 selector 为参数的 performSelector:的方法并且其他类似的方法来使用：

```cpp
SEL aSelector = @selector(run);
[aDog performSelector:aSelector];
[anAthlete performSelector:aSelector];
[aComputerSimulation performSelector:aSelector];
```

（我们使用这个技术在特殊的情况下，例如我们实现了一个使用 target-action 设计模式的对象。通常，我们直接的简单的调用该方法。）

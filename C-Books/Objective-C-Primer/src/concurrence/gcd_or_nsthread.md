# 选择 GCD 还是 NSThread?

一直以来使用 GCD 进行并发编程 而不是使用 NSThread 进行线程编程，只是因为 GCD 方便的 API 设计，却并没有仔细想想为什么 NO NSThread?

备注: 并发编程 更注重于任务的并发，忽略线程的管理；而 线程编程 则应该是两者兼具吧。

---

## GCD

在官方文档介绍里，一直推荐的是使用 GCD 来进行并发编程，而不是使用 NSThread 来进行线程编程。原因有下：

1. GCD 提供方便的 API，让我们在进行并发编程时只要关注具体的任务，而无需关注多余的线程管理；
1. GCD 帮我们提供了线程管理，我们不需要自己创建、销毁线程，同时通过 GCD 来进行并发编程，系统能够更好的利用线程资源，众所周知线程资源时有限的，在有限的资源下，GCD 能更好的发挥多线程的作用；
1. 通过 GCD 来进行资源的同步读取来代替锁操作，相对线程锁来说，在某种情况下会更好，具体文档没说明，但却指出了，GCD 代替锁可以减少锁每次的解锁操作都进入系统内核状态，这也是一种资源节省，优化；

## NSThread

苹果不推荐 NSThread 原因有下：

1. 线程比较占用内存(用户内存以及内核内存，具体可见下表 1)，如果不是很熟悉线程编程，容易导致资源的浪费；
   | Item | Approximate cost | Notes |
   | ---------------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | Kernel data structures | Approximately 1 KB | This memory is used to store the thread data structures and attributes, much of which is allocated as wired memory and therefore cannot be paged to disk. |
   | Stack space | Stack space 512 KB (secondary threads) 8 MB (OS X main thread) 1 MB (iOS main thread) | The minimum allowed stack size for secondary threads is 16 KB and the stack size must be a multiple of 4 KB. The space for this memory is set aside in your process space at thread creation time, but the actual pages associated with that memory are not created until they are needed. |
   | Creation time | Approximately 90 microseconds | This value reflects the time between the initial call to create the thread and the time at which the thread’s entry point routine began executing. The figures were determined by analyzing the mean and median values generated during thread creation on an Intel-based iMac with a 2 GHz Core Duo processor and 1 GB of RAM running OS X v10.5. |
1. 如果执行一个短的任务，线程一般执行完就退出了，这时将任务交给 GCD，也许 GCD 会将创建的线程进行重用，避免多余的创建(不管现在有没有重用功能，这都是可以优化的)；
1. 如果自己创建线程来执行一个长任务，使用 GCD 一样能完成，而且少了线程创建任务；
1. 如果实现一个类似于 AFN 那样，线程保活，然后不断的执行一些任务呢？ 不好意思，还是不推荐 NSThread, 如果你创建一个线程，并且通过 Runloop 进行保活，但却不能保证该线程一直是满载进行任务操作，这仍然是一种资源浪费，使用 GCD 一样能实现这种效果，而且还不会浪费资源， 可见新版的 AFN 已经使用 GCD 来替代原来的 NSThread 保活，所以不要在线程保活保活了，不能满载的情况下就是资源浪费。

## 总结:

所以，在平时的编程中如果没有特殊需求，使用 GCD 是最推荐的选择。

当然还有 [Operation Queues](https://developer.apple.com/library/archive/documentation/General/Conceptual/ConcurrencyProgrammingGuide/OperationObjects/OperationObjects.html#//apple_ref/doc/uid/TP40008091-CH101-SW1) , 它是基于 GCD 进行封装的类， 所以把他们归为一类了。 具体用 GCD 还是 Operation Queues, 看需求而定，Operation Queues 提供了一些 GCD 不太方便实现的功能，而 GCD 则更加快捷方便。

**PThread** ( 题外话 )
在官方文档中有这样一句话:

> For multithreaded applications, Cocoa frameworks use locks and other forms of internal synchronization to ensure they behave correctly. To prevent these locks from degrading performance in the single-threaded case, however, Cocoa does not create them until the application spawns its first new thread using the NSThread class. If you spawn threads using only POSIX thread routines, Cocoa does not receive the notifications it needs to know that your application is now multithreaded. When that happens, operations involving the Cocoa frameworks may destabilize or crash your application.

> 意思大概就是使用 GCD 和 NSThread 创建了线程时，系统会接收到一个通知，来告知 App 进入了多线程状态，这时 Cocoa 框架里的一些懒加载的锁会被初始化，增加锁操作来保证线程安全(文档中有提到在单线程的情况下，App 的 Cocoa 框架的锁都不会创建，这样相对更加高效)， 然而通过 POSIX 来创建线程时，并不会发送一个这样的通知，所以如果你的 App 之前一直是单线程在跑的话，此时进入了多线程状态，而 Cocoa 不知道，依然单着跑，结果就是很容易 crash。

更多详情请看相关资料：

1. [Threading Programming Guide](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Multithreading/Introduction/Introduction.html#//apple_ref/doc/uid/10000057i-CH1-SW1)
1. [Concurrency Programming Guide](https://developer.apple.com/library/archive/documentation/General/Conceptual/ConcurrencyProgrammingGuide/Introduction/Introduction.html#//apple_ref/doc/uid/TP40008091-CH1-SW1)

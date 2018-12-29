# 什么时候使用 Blocking Queued Connection?

## Qt::ConnectionType（信号与槽的传递方式）

- **Qt::AutoConnection** 自动连接：（默认值）如果信号在接收者所依附的线程内发射，则等同于直接连接。如果发射信号的线程和接受者所依附的线程不同，则等同于队列连接。
- **Qt::DirectConnection** 直接连接：当信号发射时，槽函数将直接被调用。无论槽函数所属对象在哪个线程，槽函数都在发射信号的线程内执行。
- **Qt::QueuedConnection** 队列连接：当控制权回到接受者所依附线程的事件循环时，槽函数被调用。槽函数在接收者所依附线程执行。也就是说：这种方式既可以在线程内传递消息，也可以跨线程传递消息
- **Qt::BlockingQueuedConnection** 与 Qt::QueuedConnection 类似，但是会阻塞等到关联的 slot 都被执行。这里出现了阻塞这个词，说明它是专门用来多线程间传递消息的。

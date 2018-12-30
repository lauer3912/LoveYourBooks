# 如何获得信号的发送者？

当多个信号连接一个槽时，有时需要判断是哪个对象发来的，那么可以调用 sender()函数获取对象指针，返回为 QObject 指针。

```cpp
QObject* sender = QObject::sender();
// 或者
QObject* sender = this->sender();
```

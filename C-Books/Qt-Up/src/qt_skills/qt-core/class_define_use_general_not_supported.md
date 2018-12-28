# 类不支持模类定义板泛型

> moc does not handle all of C++. The main problem is that class templates cannot have the `Q_OBJECT` macro.

```h
// 错误： 不支持C++的模板泛型定义
class SomeTemplate<int> : public QFrame
{
    Q_OBJECT
    ...

signals:
    void mySignal(int);
};
```

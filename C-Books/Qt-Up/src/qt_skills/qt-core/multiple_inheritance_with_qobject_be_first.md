# 多继承 QObject 必须放在前面

> Multiple Inheritance Requires QObject to Be First

> If you are using multiple inheritance, moc assumes that the first inherited class is a subclass of QObject. Also, be sure that only the first inherited class is a QObject.

```h
// 正确
class SomeClass : public QObject, public OtherClass
{
    ...
};

// 不正确
class SomeClass : public OtherClass, public QObject
{
    ...
};
```

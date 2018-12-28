# 添加更多的类信息

使用`Q_CLASSINFO()`宏给类添加更多的关于类的信息，只支持 key-value 方式

> Another macro, `Q_CLASSINFO()`, allows you to attach additional name/value pairs to the class's meta-object

示例：

```h
class MyClass : public QObject
{
    Q_OBJECT
    Q_CLASSINFO("Author", "Oscar Peterson")
    Q_CLASSINFO("Status", "Active")

public:
    MyClass(QObject *parent = 0);
    ~MyClass();
};
```

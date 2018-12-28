# 如何构建自定义 Qt 数据类型？

可以参见：[Creating Custom Qt Types](http://doc.qt.io/qt-5/custom-types.html)

主要具备三大因素：

- 公共默认的构造函数(a public default constructor)
- 公共的拷贝构造函数(a public copy constructor, and)
- 公共的析构函数(a public destructor.)

代码示例：

```cpp
class Message
{
public:
    Message();
    Message(const Message &other);
    ~Message();

    Message(const QString &body, const QStringList &headers);

    QString body() const;
    QStringList headers() const;

private:
    QString m_body;
    QStringList m_headers;
};
```

---

参见：`Q_DECLARE_METATYPE` 宏的试用

为了实现这个功能，首先必须使用 `Q_DECLARE_METATYPE()`宏。通常会将这个宏放在类的声明所在头文件的下面：

`Q_DECLARE_METATYPE(MyClass)`

示例：

MyClass.h 文件

```h
struct MyClass{
    int id;
    QString name;
};
Q_DECLARE_METATYPE(MyClass)
```

```cpp

//存储数据
MyClass myClass;
myClass.id=0;
myClass.name=QString("LiMing");

data[0]=QString("ddd");
data[1]=123;
data[3]=QVariant::fromValue(myClass);


//获取数据
QString str=data.value(0).toString();
int val=data.value(1).toInt();

if(data[3].canConvert<MyClass>())
{
    MyClass myClass=data[3].value<MyClass>();
    int id=myClass.id;
    QString name=myClass.name;
}
```

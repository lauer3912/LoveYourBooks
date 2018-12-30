# 如何让你的自定义类型也支持 QDebug 打印?

如果我们想要使用 qDebug 打印自定义类中的信息时就可以像以下这样做：

```cpp
#include <QDebug>
class Student
{
public:
    Student(const QString& nm){name = nm;}
    QString getName() const{return name;}
private:
    QString name;
};
QDebug operator<<(QDebug debug, const Student &c)
{
    debug << c.getName();
    return debug;
}
int main(int argc, char *argv[])
{
    Student student("John");
    qDebug() << student;
}
```

首先，自定义了一个类 `Student`，编写了构造函数和获取姓名的获取器。

其次，定义了"`<<`"操作符，打印名字。

最后，在 `main` 函数中创建 `Student` 的实例，并用 `qDebug()`打印该实例。

# 宏 Q_DECLARE_METATYPE 与 QVariant 如何结合使用？

## 前言

`QVariant` 这个类很神奇，或者说方便。很多时候，需要几种不同的数据类型需要传递，如果用结构体，又不大方便，容器保存的也只是一种数据类型，而 QVariant 则可以统统搞定。

## 介绍

帮助文档上说：The `QVariant` class acts like a union for the most common Qt data types.。

`QVariant` 这个类型充当着最常见的数据类型的联合。`QVariant` 可以保存很多 Qt 的数据类型，包括 QBrush、QColor、QCursor、QDateTime、QFont、QKeySequence、 QPalette、QPen、QPixmap、QPoint、QRect、QRegion、QSize 和 QString，并且还有 C++基本类型，如 int、float 等。

当然，如果支持的类型没有想要的，没关系，`QVariant` 也可以支持自定义的数据类型。**被 QVariant 存储的数据类型需要有一个默认的构造函数和一个拷贝构造函数。**

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

## 保存指针

```cpp
//保存
QVariant var=QVariant::fromValue((void*)event);

//获取
QPaintEvent* e=(QPaintEvent*)var.value<void*>();

```

# Qt 对象指针类型的动态转换用法

Qt 对象指针类型的动态转换，使用的是 Qt 自身的`qobject_cast()` 函数

> It is also possible to perform dynamic casts using `qobject_cast()` on `QObject` classes. The `qobject_cast()` function behaves similarly to the standard C++ `dynamic_cast()`, with the advantages that it doesn't require `RTTI` support and it works across dynamic library boundaries. It attempts to cast its argument to the pointer type specified in angle-brackets, returning a non-zero pointer if the object is of the correct type (determined at run-time), or 0 if the object's type is incompatible.

示例代码：

```cpp
QObject *obj = new MyWidget;
QWidget *widget = qobject_cast<QWidget *>(obj); // widget is not 0
MyWidget *myWidget = qobject_cast<MyWidget *>(obj); // myWidget is not 0
QLabel *label = qobject_cast<QLabel *>(obj); // label is 0

// 可以很方便地用到判断语句中
if (QLabel *label = qobject_cast<QLabel *>(obj)) {
    label->setText(tr("Ping"));
} else if (QPushButton *button = qobject_cast<QPushButton *>(obj)) {
    button->setText(tr("Pong!"));
}

```

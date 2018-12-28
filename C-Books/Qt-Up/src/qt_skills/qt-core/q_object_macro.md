# 所有继承 QObject 的类，建议对使用 Q_OBJECT 宏

原文：

> While it is possible to use `QObject` as a base class without the `Q_OBJECT` macro and without meta-object code, neither signals and slots nor the other features described here will be available if the `Q_OBJECT` macro is not used. From the meta-object system's point of view, a QObject subclass without meta code is equivalent to its closest ancestor with meta-object code. This means for example, that `QMetaObject::className()` will not return the actual name of your class, but the class name of this ancestor.

Therefore, we strongly recommend that all subclasses of QObject use the `Q_OBJECT` macro regardless of whether or not they actually use `signals, slots, and properties`.

说明：所有继承 QObject 的类，建议对使用 Q_OBJECT 宏。 如果不使用`Q_OBJECT`宏，那么子类所有的关于信号、槽、属性等等特性全部不可用。

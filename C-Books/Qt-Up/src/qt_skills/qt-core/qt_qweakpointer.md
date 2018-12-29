# 尽量使用弱引用计数指针 QWeakPointer

QPointer is a template class that provides guarded pointers to Qt objects and behaves like a normal C++ pointer except that it is automatically set to 0 when the referenced object is destroyed and no "dangling pointers" are produced.
QSharedPointer class holds a strong reference to a shared pointer.
QWeakPointer class holds a weak reference to a shared pointer.

QSharedPointer，它很像 std::shared_ptr，都具有拷贝构造函数、重载赋值运算符。QSharedPointer 可以通过 toWeakRef 转换成 QWeakPointer，std::shared_ptr 也可以转换成 std::weak_ptr 来检查对象是否被销毁。

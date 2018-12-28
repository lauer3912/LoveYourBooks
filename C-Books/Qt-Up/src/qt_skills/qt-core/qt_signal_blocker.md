# 如何暂时阻止发射信号？

具体引用： [QSignalBlocker](http://doc.qt.io/qt-5/qsignalblocker.html)

> 我们有一个 QCheckBox 对象，当用户检查或者删除检查，我们想要调用一个函数，以便我们将函数连接到 stateChanged ( int 状态) 信号。
> 另一方面，根据某些条件，我们也改变了代码中 QCheckBox 对象的状态，这导致了不需要的信号。
> 在某些情况下是否可以阻止发射信号？

## 优先方案

Qt5.3 引入了 QSignalBlocker 类，它在异常安全的方法中确实需要。

```cpp
if (something) {
 const QSignalBlocker blocker(someQObject);
//no signals here
}
```

这种方法等于下面的方式

```cpp
const bool wasBlocked = someQObject->blockSignals(true);
// no signals here
someQObject->blockSignals(wasBlocked);
```

## 参考讨论方案 1

你可以使用 clicked 信号，因为只有当用户真正单击复选框时才会发出该信号，而不是使用 setChecked 控件手动检查它。
如果你不想在某个特定时间发出信号，你可以使用 QObject::blockSignals 像这样：

```cpp
bool oldState = checkBox->blockSignals(true);
checkBox->setChecked(true);
checkBox->blockSignals(oldState);
```

这种方法的缺点是**所有的信号都会被阻塞**。 但我想这对于 QCheckBox 来说并不重要。

# 如何为应用添加撤销操作?

详见[QUndoCommand](http://doc.qt.io/qt-5/qundocommand.html)

## 如何建立这种机制？

1. 自定义命令类继承`QUndoCommand`
2. 重写类`QUndoCommand` 的`undo()`和`redo()`函数
3. 实际操作中，创建新的命令类对象存储到 `QUndoStack` 对象中。
4. 实际操作中，通过调用QUndoStack` 对象的undo() 方法，来达到撤销操作的目的
5. 实际操作中，通过调用QUndoStack` 对象的redo() 方法，来达到重新操作的目的

### Step1 自定义命令类继承`QUndoCommand`

```h
class ArrayCommand : public QUndoCommand
{
public:
    enum Cmd {insert, remove, replace};
    ArrayCommand(XByteArray* xData, Cmd cmd, int baPos, QByteArray newBa = QByteArray(), int len = 0, QUndoCommand* parent = nullptr);
    void undo();
    void redo();

private:
    Cmd _cmd;
    XByteArray* _xData;
    int _baPos;
    int _len;
    QByteArray _wasChanged;
    QByteArray _newBa;
    QByteArray _oldBa;
};
```

### Step2 重写类`QUndoCommand` 的`undo()`和`redo()`函数

```cpp
ArrayCommand::ArrayCommand(XByteArray* xData, Cmd cmd, int baPos, QByteArray newBa, int len, QUndoCommand* parent)
    : QUndoCommand(parent)
{
    _cmd = cmd;
    _xData = xData;
    _baPos = baPos;
    _newBa = newBa;
    _len = len;
}

void ArrayCommand::undo()
{
    switch(_cmd)
    {
    case insert:
        _xData->remove(_baPos, _newBa.length());
        break;
    case replace:
        _xData->replace(_baPos, _oldBa);
        break;
    case remove:
        _xData->insert(_baPos, _oldBa);
        break;
    }
}
```

### Step3 实际操作中，创建新的命令类对象存储到 `QUndoStack` 对象中。

```cpp
    _undoDataStack = new QUndoStack(this);
    _undoMaskStack = new QUndoStack(this);
```

```cpp
void QHexEditPrivate::replace(int index, const QByteArray & ba, const QByteArray & mask)
{
    _undoDataStack->push(new ArrayCommand(&_xData, ArrayCommand::replace, index, ba, ba.length()));
    _undoMaskStack->push(new ArrayCommand(&_xMask, ArrayCommand::replace, index, mask, mask.length()));
    resetSelection();
    emit dataChanged();
    emit dataEdited();
}

```

### 实际操作中，通过调用QUndoStack` 对象的undo() 方法，来达到撤销操作的目的

```cpp
void QHexEditPrivate::undo()
{
    if(!_undoDataStack->canUndo() || !_undoMaskStack->canUndo())
        return;
    _undoDataStack->undo();
    _undoMaskStack->undo();
    emit dataChanged();
    emit dataEdited();
    setCursorPos(_cursorPosition);
    update();
}
```

### 实际操作中，通过调用QUndoStack` 对象的redo() 方法，来达到重新操作的目的

```cpp
void QHexEditPrivate::redo()
{
    if(!_undoDataStack->canRedo() || !_undoMaskStack->canRedo())
        return;
    _undoDataStack->redo();
    _undoMaskStack->redo();
    emit dataChanged();
    emit dataEdited();
    setCursorPos(_cursorPosition);
    update();
}
```
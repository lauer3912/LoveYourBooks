# 用 QVariant 来保存指针

## 保存指针

```cpp
//保存
QVariant var=QVariant::fromValue((void*)event);

//获取
QPaintEvent* e=(QPaintEvent*)var.value<void*>();

```

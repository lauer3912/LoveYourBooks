# 函数指针不能作为信号和槽的参数

一般情况下，直接使用函数指针是会提示语法错误的。

```cpp
class SomeClass : public QObject
{
    Q_OBJECT

public slots:
    void apply(void (*apply)(List *, void *), char *); // 语法错误！WRONG
};
```

但可以通过以下方式绕过该机制

```cpp
typedef void (*ApplyFunction)(List *, void *);

class SomeClass : public QObject
{
    Q_OBJECT

public slots:
    void apply(ApplyFunction, char *);  // 正确
};
```

建议：有时用继承和虚拟函数替换函数指针可能会更好。

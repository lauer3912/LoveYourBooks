# 嵌套类中的类不能有信号和槽机制

```cpp
class A
{
public:
    class B
    {
        Q_OBJECT

    public slots:   // 错误！WRONG
        void b();
    };
};
```

以下都是正常运行的。如果，嵌套类中使用信号和槽，信号和槽就不会有效

```cpp

// 编译正常
class CustomObject {
public:
    class CustomItem {
        Q_OBJECT
    public:
        explicit CustomItem(){}
        ~ CustomItem(){}
    };
};
```

```cpp
class CustomObject {
    Q_OBJECT // Error: Class contains Q_OBJECT macro but does not inherit from QObject
public:
    class CustomItem {
        Q_OBJECT
    public:
        explicit CustomItem(){}
        ~ CustomItem(){}
    };
};
```

```cpp
class CustomObject : public QObject {
    Q_OBJECT
public:
    class CustomItem {
        Q_OBJECT // Error: Meta object features not supported for nested classes
    public:
        explicit CustomItem(){}
        ~ CustomItem(){}
    private slots:
        void on_clicked();
    };
};
```

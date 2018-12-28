# 嵌套 QOjbect 子类中的类不能使用宏 Q_OBJECT

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

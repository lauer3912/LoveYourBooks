# 使用宏 Q_OBJECT, 类必须继承 QObject 或 QObject 子类

// Error: Class contains Q_OBJECT macro but does not inherit from QObject

```cpp
class CustomObject {
    Q_OBJECT // Error: Class contains Q_OBJECT macro but does not inherit from QObject
public:
    explicit CustomObject();
    ~CustomObject();
};
```

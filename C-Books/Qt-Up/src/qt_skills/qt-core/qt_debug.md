# 如何使用 QDebug 打印调试信息

引入 `#include <QDebug>`

```cpp
#include <QDebug>

void info() {
    qDebug() << "Date:" << QDate::currentDate();
    qDebug() << "Types:" << QString("String") << QChar('x') << QRect(0, 10, 50, 40);
    qDebug() << "Custom coordinate type:" << coordinate;
}

```

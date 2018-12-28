# Qt 的迭代器接口如何使用？

- [QSequentialIterable](http://doc.qt.io/qt-5/qsequentialiterable.html)
- [QAssociativeIterable Qt 关联容器迭代器](http://doc.qt.io/qt-5/qassociativeiterable.html#details)

## QSequentialIterable

QSequentialIterable 类是 QVariant 中容器的可迭代接口。
The QSequentialIterable class is an iterable interface **for a container in a QVariant**.

This class allows several methods of accessing the elements of a container held within a QVariant. An instance of QSequentialIterable can be extracted from a QVariant if it can be converted to a QVariantList.

```cpp
QList<int> intList = {7, 11, 42};

QVariant variant = QVariant::fromValue(intList);
if (variant.canConvert<QVariantList>()) {
    QSequentialIterable iterable = variant.value<QSequentialIterable>();
    // Can use foreach:
    foreach (const QVariant &v, iterable) {
        qDebug() << v;
    }
    // Can use C++11 range-for:
    for (const QVariant &v : iterable) {
        qDebug() << v;
    }
    // Can use iterators:
    QSequentialIterable::const_iterator it = iterable.begin();
    const QSequentialIterable::const_iterator end = iterable.end();
    for ( ; it != end; ++it) {
        qDebug() << *it;
    }
}
```

## QAssociativeIterable

QAssociativeIterable 类是 QVariant 中关联容器的可迭代接口。
The QAssociativeIterable class is an iterable interface **for an associative container in a QVariant**.

```cpp
QHash<int, QString> mapping;
mapping.insert(7, "Seven");
mapping.insert(11, "Eleven");
mapping.insert(42, "Forty-two");

QVariant variant = QVariant::fromValue(mapping);
if (variant.canConvert<QVariantHash>()) {
    QAssociativeIterable iterable = variant.value<QAssociativeIterable>();
    // Can use foreach over the values:
    foreach (const QVariant &v, iterable) {
        qDebug() << v;
    }
    // Can use C++11 range-for over the values:
    for (const QVariant &v : iterable) {
        qDebug() << v;
    }
    // Can use iterators:
    QAssociativeIterable::const_iterator it = iterable.begin();
    const QAssociativeIterable::const_iterator end = iterable.end();
    for ( ; it != end; ++it) {
        qDebug() << *it; // The current value
        qDebug() << it.key();
        qDebug() << it.value();
    }
}
```

# 判断 QVariant 类型是否可以转换？

```h
bool QVariant::canConvert(int targetTypeId) const
```

具体参考： [http://doc.qt.io/qt-5/qvariant.html](http://doc.qt.io/qt-5/qvariant.html)

## 示例 1：

```cpp
QDataStream out(...);
QVariant v(123);                // The variant now contains an int
int x = v.toInt();              // x = 123
out << v;                       // Writes a type tag and an int to out
v = QVariant("hello");          // The variant now contains a QByteArray
v = QVariant(tr("hello"));      // The variant now contains a QString
int y = v.toInt();              // y = 0 since v cannot be converted to an int
QString s = v.toString();       // s = tr("hello")  (see QObject::tr())
out << v;                       // Writes a type tag and a QString to out
...
QDataStream in(...);            // (opening the previously written stream)
in >> v;                        // Reads an Int variant
int z = v.toInt();              // z = 123
qDebug("Type is %s",            // prints "Type is int"
        v.typeName());
v = v.toInt() + 100;            // The variant now hold the value 223
v = QVariant(QStringList());

QVariant v = 42;

v.canConvert<int>();              // returns true
v.canConvert<QString>();          // returns true

MyCustomStruct s;
v.setValue(s);

v.canConvert<int>();              // returns false
v.canConvert<MyCustomStruct>();   // returns true
```

## 示例 2

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

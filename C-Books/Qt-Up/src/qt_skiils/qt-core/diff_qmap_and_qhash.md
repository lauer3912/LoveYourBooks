# QMap 与 QHash 有什么区别？

关联容器可以保存任意多个具有相同类型的项，且它们由一个键索引。Qt 提供两个主要的关联容器类：QMap<K, T>和 QHash<K, T>。

QMap<K, T>是一个以升序键顺序存储键值对的数据结构。这种排列使它可以提供良好的查找插入性能及键序的迭代。在内部，QMap<K, T>是作为一个跳越列表(skip-list)来实现执行的。
在映射中插入项的一种简单方式是调用 insert():

```cpp
QMap<QString, int> map;
map.insert("eins", 1);
map.insert("sieben", 7);
map.insert("dreiundzwanzig", 23);
```

另外，也可以像下面一样，给一个指定的键赋值：

```cpp
map["eins"] = 1;
map["sieben"] = 7;
map["dreiundzwanzig"] = 23;
```

\[]操作符即可以用于插入也可以用于检索。如果在非常量映射中使用\[]为一个不存在的键检索值，则会用给定的键和空值创建一个新的项。为了避免意外的创建空值，可以使用 value()函数代替[]操作符来获得项。

```cpp
int val = map.value("dreiundzwanzig")
```

如果键不存在，则利用值类型的默认构造函数，将返回一个默认值，同时不会创建新的项。对于基本类型和指针类型，将返回 0 值。我们可以指定另一默认值作为 value()的第二个参数，例如：

```cpp
int seconds = map.value("delay", 30);
```

这相当于：

```cpp
int seconds = 30;
if (map.contains("delay");
    seconds = map.value("delay");
```

QMap<K, T>的 K 和 T 数据类型可以是与 int、double、指针类型、有默认构造函数的类、复制构造函数和赋值操作符相似的基本数据类型。
此外，K 类型必须提供 operator<()，因为 QMap<K, T>要使用这个操作符以提升键序顺序存储项。

QMap<K, T>的 K 和 T 有一对方便的函数 keys()和 values()，它们在处理小数据集时显的特别有用。它们分别返回映射键的 QList 和映射值的 QList。

映射通常都是单一值的：如果赋予一个现有的键一个新值，则原有的旧值将被该新值取代，以确保两个项不会共有同一个键。
通过使用 insertMulti()函数或者 QMlltiMap<K, T>方便的子类，可以让多个键值对有相同的键。
QMap<K, T>重载了 value(const K &), 返回一个给定键多有值的 QList 列表。例如：

```cpp
QMultiMap<int, QString> multiMap;
multiMap.insert(1, "one");
multiMap.insert(1, "eins");
multiMap.insert(1, "uno");
QList<QString> vals = multiMap.values(1);
```

QHash<K, T>是一个在哈希表中存储键值对的数据结构。
它的接口几乎与 QMap<K, T>相同，但是与 QMap<K, T>相比，它对 K 的模板类型有不同的要求，而且它提供了比 QMap<K, T>更快的查找功能。

除了对存储在容器类中的所有值类型的一般要求，QHash<K, T>中 K 的值类型还需要提供一个 operator==()，并需要一个能够为键返回哈希值的全局 qHash()函数的支持。
Qt 已经为 qHash()函数提供了对整型、指针型、QChar、QString 以及 QByteArray。

QHash<K, T>为它内部的哈希表自动分配最初的存储区域，并在有项被插入或者删除时重新划分所分配的存储区域的大小。
也可以通过调用 reserve()或者 squeeze()来指定或者压缩希望存储到哈希表中的项的数目，以进行性能调整。
通常的做法是利用我们预期的最大的项的数目来条用 reserve(),然后插入数据，最后如果有多出的项，则调用 squeeze()以使内存的使用减到最小。

虽然哈希表通常都是单一值的，但是使用 insertMulti()函数或者 MultiHash<K, T>方便的子类，也可以将多个值赋给同一个键。

除了 QHash<K, T>之外，Qt 还提供了一个用来高速缓存与键相关联的对象的 QCache<K, T>类以及仅仅存储键的 QSet<K>容器。
在内部，它们都依赖于 QHash<K, T>，且都像 QHash<K, T>一样对 K 的类型有相同的要求。

最简便的遍历存储在关联容器中多有键值对的方式是使用 Java 风格的迭代器。因为迭代器必须能同时访问键和值，针对关联容器的 Java 风格的迭代器与连续容器的在运作方式有些差异。只要区别在于 next()和 previous()函数返回一个代表键值对的对象，而不是一个简单的值。我们可以使用 key()和 value()分别从这个对象中获得键和值。例如：

```cpp
QMap<QString, int> map;
...
int sum = 0;
QMapIterator<QString, int> i(map）；
while (i.hasNext())
    sum += i.next().value();
```

如果需要同时存取键和值，可以先忽略 next()或 previous()的返回值并使用迭代器的 key()和 value()函数，它们都是针对最后被跳过的项进行操作的：

```cpp
QMapIterator<QString, int> i(map);
while(i.hasNext()){
    i.next();
    if (i.value() > largestValue){
        largestKey = i.key();
        largestValue = i.value();
    }
}
```

QMap 提供了一个从类项为 key 的键到类项为 T 的直的映射，通常所存储的数据类型是一个键对应一个直，并且按照 Key 的次序存储数据，
这个类也支持一键多值的情况，用类 QMultiMap

QHash 具有和 QMap 几乎完全一样的 APi，此类维护这一张哈希表，表的大小和数据项是自适应的，QHash 是以任意的顺序住址他的数据，，当然了他也是可以支持一键多值的，QMultiHash

两种之间的区别是：

- QHash 查找速度上显著于 QMap
- QHash 以任意的方式进行存储，而 QMap 则是以 key 顺序进行存储
- Qhash 的键类型必须提供 operator==()和一个全局的 qHash(key)函数。而 QMap 的键类型 key 必须提供 operator<()函数

他们同样也是有两种风格的迭代容器。用来进行遍历的。
STL 风格的

QMap<key,T> QMap<key,T>::const_iterator QMap<key,T>::iterator//同样中间那个也是只读的，最后那个是读写的。
下面以一个例子来进行说明：

```cpp
#include <QDebug>

int main(int argc, char \*argv[])
{
    QMap<QString, QString> map;
    map.insert("beijing", "111");
    map.insert("shanghai", "021");
    map.insert("tianjin", "022");
    map.insert("chongqing", "023");
    map.insert("jinan", "0531");
    map.insert("wuhan", "027");

    QMap<QString, QString>::const_iterator i;
    for( i=map.constBegin(); i!=map.constEnd(); ++i)
    qDebug() << i.key() <<" " << i.value();

    QMap<QString, QString>::iterator mi;
    mi = map.find("beijing");
    if(mi != map.end())
    mi.value() = "010";
    QMap<QString, QString>::const_iterator modi;
    qDebug() << "";
    for( modi=map.constBegin(); modi!=map.constEnd(); ++modi)
    qDebug() << modi.key() <<" " << modi.value();
 return 0;
}
```

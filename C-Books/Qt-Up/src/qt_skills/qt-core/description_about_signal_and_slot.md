# 信号槽的调用流程原理是怎样的？

信号槽的调用流程:

1. moc 查找头文件中的 signals，slots，标记出信号和槽
2. 将信号槽信息存储到类静态变量 staticMetaObject 中，并且按声明顺序进行存放，建立索引。
3. 当发现有 connect 连接时，将信号槽的索引信息放到一个 map 中，彼此配对。
4. 当调用 emit 时，调用信号函数，并且传递发送信号的对象指针，元对象指针，信号索引，参数列表到 active 函数
5. 通过 active 函数找到在 map 中找到所有与信号对应的槽索引
6. 根据槽索引找到槽函数，执行槽函数。

示例程序
新建控制台应用程序，再添加一个新类 SignalsAndSlots3，各自定义一个信号和槽，代码如下：

```cpp
// signalsandslots3.h

class SignalsAndSlots3 : public QObject
{
    Q_OBJECT
public:
    explicit SignalsAndSlots3(QObject *parent = 0);

signals:
    void sigPrint(const QString& text);

public slots:
    void sltPrint(const QString& text);
};
```

```cpp
//signalsandslots3.cpp

#include <QDebug>
#include "signalsandslots3.h"

SignalsAndSlots3::SignalsAndSlots3(QObject *parent) : QObject(parent)
{
    connect(this, SIGNAL(sigPrint(QString)), this, SLOT(sltPrint(QString)));
    emit sigPrint("Hello");
}

void SignalsAndSlots3::sltPrint(const QString &text)
{
    qDebug() << text;
}
```

```cpp
//main.cpp

#include <QCoreApplication>
#include "signalsandslots3.h"

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    SignalsAndSlots3 s;

    return a.exec();
}
```

本节为了说明原理，所以只写了最简单的信号槽。

编译运行程序，在控制台会输出 Hello 字样。

## Makefile 文件

现在我们打开 Qt 自动生成的 Makefile.Debug 文件。找到下面这一行：

SOURCES = F:\Study\Qt\Projects\QtShareCode\chapter2\2-3\SignalsAndSlots3\main.cpp \
F:\Study\Qt\Projects\QtShareCode\chapter2\2-3\SignalsAndSlots3\signalsandslots3.cpp debug\moc_signalsandslots3.cpp

关键看加粗的部分，我们看到 signalsandslots3.cpp 和 moc_signalsandslots3.cpp 作为源文件一起进行编译。

由此可知，Qt 又额外生成了 moc_signalsandslots3.cpp 文件，其名称为，同名源文件前加上了 moc 前缀。

## moc 预编译器

moc(Meta-Object Compiler)元对象预编译器。

moc 读取一个 c++头文件。如果它找到包含 Q*OBJECT 宏的一个或多个类声明，它会生成一个包含这些类的元对象代码的 c++源文件，并且以 moc*作为前缀。

信号和槽机制、运行时类型信息和动态属性系统需要元对象代码。

由 moc 生成的 c++源文件必须编译并与类的实现联系起来。

通常，moc 不是手工调用的，而是由构建系统自动调用的，因此它不需要程序员额外的工作。

2.3.4 Q_OBJECT 宏

```cpp
#define Q_OBJECT \
public: \
    Q_OBJECT_CHECK \
    QT_WARNING_PUSH \
    Q_OBJECT_NO_OVERRIDE_WARNING \
    static const QMetaObject staticMetaObject; \
    virtual const QMetaObject *metaObject() const; \
    virtual void *qt_metacast(const char *); \
    virtual int qt_metacall(QMetaObject::Call, int, void **); \
    QT_TR_FUNCTIONS \
private: \
    Q_OBJECT_NO_ATTRIBUTES_WARNING \
    Q_DECL_HIDDEN_STATIC_METACALL static void qt_static_metacall(QObject *, QMetaObject::Call, int, void **); \
    QT_WARNING_POP \
    struct QPrivateSignal {}; \
    QT_ANNOTATE_CLASS(qt_qobject, "")
```

我们 都知道宏会在预编译期被具体的字符串所代替，那么我们在头文件中用到的 Q_OBJECT 宏就会被展开为上面的代码。

你可以在 signalsandslots3.h 中用上面的代码替换掉 Q_OBJECT ，你会发现还需要实现 Q_OBJECT 扩展后所带来的变量和函数的定义。而这些定义都已经被写入到了 moc_signalsandslots3.cpp 文件中了，这也就是为什么在 Makefile 中需要将 moc_signalsandslots3.cpp 一起编译的原因了。否则，这个类是不完整的，那肯定也是不可能编译通过的。

2.3.5 moc_signalsandslots3.cpp
从头文件中得出，我们首先需要定义

```cpp
static const QMetaObject staticMetaObject;
```

你需要从下往上看代码

```cpp
/*
6.存储类中的函数及参数信息
*/
struct qt_meta_stringdata_SignalsAndSlots3_t {
    QByteArrayData data[5];//函数加参数共5个
    char stringdata0[41];//总字符串长41
};
```

```cpp
/*
5.切分字符串
*/
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_SignalsAndSlots3_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
```

```cpp
/*
4.初始化qt_meta_stringdata_SignalsAndSlots3，并且将所有函数拼接成字符串，中间用\0分开
*/
static const qt_meta_stringdata_SignalsAndSlots3_t qt_meta_stringdata_SignalsAndSlots3 = {
    {
QT_MOC_LITERAL(0, 0, 16), // "SignalsAndSlots3" (索引，偏移量，偏移长度)，类名
QT_MOC_LITERAL(1, 17, 8), // "sigPrint"
QT_MOC_LITERAL(2, 26, 0), // ""
QT_MOC_LITERAL(3, 27, 4), // "text"
QT_MOC_LITERAL(4, 32, 8) // "sltPrint"
    },
    "SignalsAndSlots3\0sigPrint\0\0text\0"//注意这是一行字符串
    "sltPrint"
};
#undef QT_MOC_LITERAL
```

```cpp
/*
3.存储元对象信息，包括信号和槽机制、运行时类型信息和动态属性系统
*/
static const uint qt_meta_data_SignalsAndSlots3[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
       2,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: name, argc, parameters, tag, flags
              1,    1,   24,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
              4,    1,   27,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void, QMetaType::QString,    3,

 // slots: parameters
    QMetaType::Void, QMetaType::QString,    3,

       0        // eod
};
```

```cpp
/*
2.执行对象所对应的信号或槽，或查找槽索引
*/
void SignalsAndSlots3::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        SignalsAndSlots3 *_t = static_cast<SignalsAndSlots3 *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->sigPrint((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 1: _t->sltPrint((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        void **func = reinterpret_cast<void **>(_a[1]);
        {
            typedef void (SignalsAndSlots3::*_t)(const QString & );
            if (*reinterpret_cast<_t *>(func) == static_cast<_t>(&SignalsAndSlots3::sigPrint)) {
                *result = 0;
                return;
            }
        }
    }
}
```

```cpp
/*
1.首先初始化静态变量staticMetaObject，并为QMetaObject中的无名结构体赋值
*/
const QMetaObject SignalsAndSlots3::staticMetaObject = {
    { &QObject::staticMetaObject, //静态变量地址
      qt_meta_stringdata_SignalsAndSlots3.data,
      qt_meta_data_SignalsAndSlots3,
      qt_static_metacall, //用于执行对象所对应的信号或槽，或查找槽索引
      Q_NULLPTR,
      Q_NULLPTR
    }
};

```

从上面的代码中，我们得知 Qt 的元对象系统：信号槽，属性系统，运行时类信息都存储在静态对象 staticMetaObject 中。

接下来是对另外三个公有接口的定义，在你的代码中也可以直接调用下面的函数哦

```cpp
//获取元对象，可以调用this->metaObject()->className();获取类名称
const QMetaObject *SignalsAndSlots3::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

//这个函数负责将传递来到的类字符串描述，转化为void*
void *SignalsAndSlots3::qt_metacast(const char *_clname)
{
    if (!_clname) return Q_NULLPTR;
    if (!strcmp(_clname, qt_meta_stringdata_SignalsAndSlots3.stringdata0))
        return static_cast<void*>(const_cast< SignalsAndSlots3*>(this));
    return QObject::qt_metacast(_clname);
}

//调用方法
int SignalsAndSlots3::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 2)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 2;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 2)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 2;
    }
    return _id;
}
```

接下来，我们发现在头文件中声明的信号，其真正定义是在这里，这也是为什么 signal 不需要我们定义的原因。

````cpp
// SIGNAL 0
void SignalsAndSlots3::sigPrint(const QString & _t1)
{
    void *_a[] = { Q_NULLPTR, const_cast<void*>(reinterpret_cast<const void*>(&_t1)) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}

```cpp
2.3.6 关键字
2.3.6.1 signals

```cpp
# define QT_ANNOTATE_ACCESS_SPECIFIER(x)
# define Q_SIGNALS public QT_ANNOTATE_ACCESS_SPECIFIER(qt_signal)
# define signals Q_SIGNALS
````

看到了吗，如果 signals 被展开的话就是 public，所以所有的信号都是公有的，也不需要像槽一样加 public，protected，private 的限定符。

2.3.6.2 slots

```cpp
# define QT_ANNOTATE_ACCESS_SPECIFIER(x)
# define Q_SLOTS QT_ANNOTATE_ACCESS_SPECIFIER(qt_slot)
# define slots Q_SLOTS
```

slots 和 signals 一样，只是没有了限定符，所以它是否可以被对象调用，就看需求了。

2.3.6.3 emit
它的宏定义：# define emit

emit 后面也没有字符串！当它被替换的时候，程序其实就是调用了 sigPrint()函数，而不是真正意义上的发送一个信号，有很多初学者都是认为当 emit 的时候，Qt 会发信号，所以才会有很多人问“当 emit 之后，会不会立即执行其后面的代码”。当然，如果想让 emit 后面的代码不需要等槽函数执行完就开始执行的话，可以设置 connect 第 5 个参数。

Qt 之所以使用# define emit，是因为编译器并不认识 emit 啊，所以把它定义成一个空的宏就可以通过编译啦。

2.3.7 信号槽的调用流程
好，通过以上的代码和分享我们来总结一下具体流程。

moc 查找头文件中的 signals，slots，标记出信号和槽
将信号槽信息存储到类静态变量 staticMetaObject 中，并且按声明顺序进行存放，建立索引。
当发现有 connect 连接时，将信号槽的索引信息放到一个 map 中，彼此配对。
当调用 emit 时，调用信号函数，并且传递发送信号的对象指针，元对象指针，信号索引，参数列表到 active 函数
通过 active 函数找到在 map 中找到所有与信号对应的槽索引
根据槽索引找到槽函数，执行槽函数。
以上，便是信号槽的整个流程，总的来说就是一个“注册-索引”机制，并不存在发送系统信号之类的事情。

注意，我们本节讲的东西都是以 connect 第五个参数是默认为前提的。

Qt 通过信号和槽机制，使得程序员在创建类时可以只关注类要做什么，这使得一个类真正具有了独立性。信号槽让它们之间自由的，动态的进行交互，从而使整个系统运行流畅，而你也不需要再插手管理。

欢迎关注小豆君的微信公众号：小豆君，只要关注，便可加入小豆君为大家创建的 C++\Qt 交流群，方便讨论学习。

编辑于 2017-12-19
C++
Qt（C++ 开发框架）
编程

以上，便是信号槽的整个流程，总的来说就是一个“注册-索引”机制，并不存在发送系统信号之类的事情。

Qt 通过信号和槽机制，使得程序员在创建类时可以只关注类要做什么，这使得一个类真正具有了独立性。信号槽让它们之间自由的，动态的进行交互，从而使整个系统运行流畅，而你也不需要再插手管理。

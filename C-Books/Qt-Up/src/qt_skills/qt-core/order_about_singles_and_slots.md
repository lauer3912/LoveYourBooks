# 信号和槽被激活的调用次序是随机的吗？

答案： 不是随机的。

想了解的更明白，应该细细读读下文。

Qt 最明显区别于其它开发框架的特征：信号和槽

## 信号槽的基本概念

在面向对象的编程方法中，都会创建很多的实例，每个实例都是单独的，要想每个实例能够协同合作，那么就会需要一种对象间传递消息的机制，在很多框架中都采用回调函数来进行对象间信息传递。

回调是一个指向函数的指针，如果想要一个处理函数通知一些事件，你需要将这个指针传递给处理函数。处理函数在适当时间调用回调函数。MFC 就是使用的回调函数，但回调可能是不直观的，不易于理解的，并且也不能保证是类型安全的。

Qt 为了消除回调函数等的弊端，从而 Qt 开发了一种新的消息传递机制，即信号和槽。

例如，当我们要求鼠标点击某个按钮时，对应的窗口就需要关闭，那么这个按钮就会发出一个关闭信号，而窗口接收到这个信号后执行关闭窗口。那么，这个信号就是按钮被点击，而槽就是窗口执行关闭函数。

可以将信号和槽理解成“命令-执行”，即信号就是命令，槽就是执行命令。

![](qt_skills/qt-core/images/single_and_slot.jpg)

## 信号

当一个对象的内部状态发生改变时，如果其它对象对它的状态需要有所反应，这时就应该让这个类发出状态改变的信号。

- 声明信号使用 `signals` 关键字
- 发送信号使用 `emit` 关键字

注意：

>

1. 所有的信号声明都是公共的，所以 Qt 规定不能在 signals 前面加 public,private, protected。
2. 所有的信号都没有返回值，所以返回值都用 void。
3. 所有的信号都不需要定义。
4. 必须直接或间接继承自 QOBject 类，并且开头私有声明包含 Q_OBJECT。
5. 当一个信号发出时，会立即执行其槽函数，等待槽函数执行完毕后，才会执行后面的代码，如果一个信号链接了多个槽，那么会等所有的槽函数执行完毕后才执行后面的代码，槽函数的执行顺序是按照它们链接时的顺序执行的。
6. 在链接信号和槽时，可以设置链接方式为：在发出信号后，不需要等待槽函数执行完，而是直接执行后面的代码。
7. 发出信号使用 emit 关键字。
8. 信号参数的个数不得少于槽参数的个数。

## 槽

槽其实就是普通的 C++函数，它唯一特点就是能和信号链接。当和它链接的信号被发出时，这个槽就会被调用。

声明槽可以使用：public/protected/private slots:

以上是 Qt4 的做法，在 Qt5 中你也不需要使用这些声明，每个函数都可以被当作是槽函数，而且还可以使用 Lambda 表达式来作为槽。不过为了程序的可读性，我还是推荐槽函数要声明一下。

## 连接信号和槽

使用 `connect` 函数连接信号和槽.

### 原型 1

```cpp
static QMetaObject::Connection connect(
    const QObject *sender, //信号发送对象指针
    const char *signal,    //信号函数字符串，使用SIGNAL()
    const QObject *receiver, //槽函数对象指针
    const char *member, //槽函数字符串，使用SLOT()
    Qt::ConnectionType = Qt::AutoConnection//连接类型，一般默认即可
);

//例如
connect(pushButton, SIGNAL(clicked()), dialog,  SLOT(close()));
```

Qt4 和 Qt5 都可以使用这种连接方式

### 原型 2

```cpp
static QMetaObject::Connection connect(
    const QObject *sender, //信号发送对象指针
    const QMetaMethod &signal,//信号函数地址
    const QObject *receiver, //槽函数对象指针
    const QMetaMethod &method,//槽函数地址
    Qt::ConnectionType type = Qt::AutoConnection//连接类型，一般默认即可
);

//例如
connect(pushButton, QPushButton::clicked, dialog,  QDialog::close);
```

Qt5 新增这种连接方式，这使得在编译期间就可以进行拼写检查，参数检查，类型检查，并且支持相容参数的兼容性转换。

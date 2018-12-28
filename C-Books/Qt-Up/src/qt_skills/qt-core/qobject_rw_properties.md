# Qt 类 Property 属性读写封装

## 简介

Qt 提供一个复杂属性系统，类似于其它编译器供应商所提供的（Property System）。然而，作为一个与编译器和平台无关的库，Qt 不依赖于那些非标准的编译器特性，如：\_property 或[property]。Qt 的解决方案适用于 Qt 支持平台下的任何标准 C++编译器。它基于元对象系统（Meta Object Sytstem），也通过信号和槽提供对象间通讯机制。

Qt 的属性系统为 Qt 的类添加了更加实惠的功能。有助于 Qt 对象状态变化，变化通知、封装等等操作。

## 声明属性的要求

为了声明一个属性，在继承 QObject 的类中使用 `Q_PROPERTY()`宏.

```cpp
Q_PROPERTY(type name
           (READ getFunction [WRITE setFunction] |
            MEMBER memberName [(READ getFunction | WRITE setFunction)])
           [RESET resetFunction]
           [NOTIFY notifySignal]
           [REVISION int]
           [DESIGNABLE bool]
           [SCRIPTABLE bool]
           [STORED bool]
           [USER bool]
           [CONSTANT]
           [FINAL])
```

Here are some typical examples of property declarations taken from class QWidget.
以下是摘自 QWidget 类的典型属性声明的例子：

```cpp
Q_PROPERTY(bool focus READ hasFocus)
Q_PROPERTY(bool enabled READ isEnabled WRITE setEnabled)
Q_PROPERTY(QCursor cursor READ cursor WRITE setCursor RESET unsetCursor)
```

下面的示例，展示了如何使用 MEMBER 关键字将类成员变量导出为 Qt 属性。注意：必须被指定一个 NOTIFY 信号以允许 QML 属性绑定。

```cpp
    Q_PROPERTY(QColor color MEMBER m_color NOTIFY colorChanged)
    Q_PROPERTY(qreal spacing MEMBER m_spacing NOTIFY spacingChanged)
    Q_PROPERTY(QString text MEMBER m_text NOTIFY textChanged)
    ...
signals:
    void colorChanged();
    void spacingChanged();
    void textChanged(const QString &newText);

private:
    QColor  m_color;
    qreal   m_spacing;
    QString m_text;
```

## 一个属性的行为就像一个类的数据成员，但它有通过元对象系统访问的附加特性。

- 如果没有指定 `MEMBER` 关键字，则需要一个 `READ` 访问函数。用于读取属性值。理想的情况下，一个 const 函数用于此目的，并且它必须返回属性类型或类型的 const 引用。如：`QWidget::focus` 是一个只读属性，通过 `READ` 函数 `QWidget::hasFocus()`访问。
- 一个 `WRITE` 访问函数是**可选的**，用于设置属性值。它必须返回 `void` 并且必须接受一个参数，该参数是属性类型，或此类型的指针，引用，例如：`QWidget::enabled` 具有 `WRITE` 函数 `QWidget::setEnabled()`。只读属性不需要 `WRITE` 函数，例如：`QWidget::focus` 没有 `WRITE` 函数
- 如果 `READ` 访问函数没有被指定，则 `MEMBER` 变量关联是必须的。这使得给定的成员变量可读可写，而不需要创建 `READ` 和 `WRITE` 访问函数。如果需要控制变量访问，除了使用 `MEMBER` 变量关联外，仍然可以使用 `READ` 和 `WRITE` 函数（但不要同时使用）
- 一个 `RESET` 函数是**可选的**，用于将属性设置为上下文指定的默认值。例如：`QWidget::cursor` 有典型的 `READ` 和 `WRITE` 函数，`QWidget::cursor()`和 `QWidget::setCursor()`，同时也有一个 `RESET` 函数 `QWidget::unsetCursor()`，因为没有 `QWidget::setCursor()`调用将 `cursor` 属性重置为上下文默认的值。`RESET` 函数必须返回 `void` 类型，并且不带任何参数。
- 一个 `NOTIFY` 信号是**可选的**。如果定义了 `NOTIFY`，则需要在类中指定一个已存在的信号，该信号在属性值改变时发射。`MEMBER` 变量的 `NOTIFY` 信号必须是 0 个或一个参数，而且必须与属性的类型相同。参数保存的是属性的新值。`NOTIFY` 信号应该仅当属性值真正的发生变化时发射，以避免绑定在 `QML` 不必要的重新评估。例如：当需要一个没有显式 `setter` 的 `MEMBER` 属性时，Qt 会自动发射信号。
- 一个 `REVISION` 数字是**可选的**。如果包含了该关键字，它定义了在 API 特定修订中使用的属性和通知器信号（通常是 QML）；如果没有包含，它默认为 `0`。
- `DESIGNABLE` 属性指定了该属性在 GUI 设计器（如 `Qt Designer`）的属性编辑器中是否可见。大多数的属性是 `DESIGNABLE` （默认为 true）。除了 true 或 false，还可以指定 boolean 成员函数。
- `SCRIPTABLE` 属性表明这个属性是否可以被一个脚本引擎操作（默认是 true）。除了 true 或 false，你还可以指定 boolean 成员函数。
- `STORED` 属性表明了该属性是否被认为是自己已存在的或是依赖于其它值。它也表明在保存对象状态时，是否必须保存此属性的值。大多数属性是 STORED（默认为 true）。但是例如：`QWidget::minmunWidth()`的 `STROED` 为 false，因为它的值从 `QWidget::minimumSize()`（类型为 `QSize`）中的宽度部分取得。
- `USER` 属性指定了在类中属性是否被设计为面向用户或可编辑的。通常情况下，每一个类只有一个 `USER` 属性（默认为 false）。例如： `QAbstractButton::checked` 是按钮的用户可编辑属性（checkable）。注意：`QItemDelegate` 获取和设置 `widget` 的 `USER` 属性。
- `CONSTANT` 属性的存在表明属性是一个常量值。对于给定的 object 实例，常量属性的 `READ` 函数在每次被调用时必须返回相同的值。不同的 object 实例该常量值可能会不同。一个常量属性不能具有 `WRITE` 函数或 `NOYIFY` 信号。
- `FINAL` 属性的存在表明属性不能被派生类所重写。在有些情况下，这可以用于效率优化，但不能被 moc 强制执行。必须注意不能重写一个 `FINAL` 属性。
  `READ`,`WRITE`,`RESET` 函数能被继承，也能是 `virtual` 的。当多重继承时，它们必须来自第一个继承的类。

## 属性类型可以是 QVariant 支持的任意类型，或者是用户定义的类型。在这个例子中，类 QDate 被看作是一个用户定义的类型。

```cpp
Q_PROPERTY(QDate date READ getDate WRITE setDate)
```

因为 `QDate` 是用户自定义的，必须包含有属性声明的头文件。

由于历史原因，QMap 和 QList 作为属性类型等同于 `QVarinatMap` 和 `QVarintList`.
For historical reasons, QMap and QList as property types are synonym of QVariantMap and QVariantList.

对于 QMap、QList 和 QValueList 属性，属性的值是一个 QVariant，它包含整个 list 或 map。

注意：Q_PROPERTY 字符串不能包含逗号，因为逗号会分割宏的参数。因此，你必须使用 QVarinatMap 作为属性的类型而不是 QMap

## 通过元对象系统读写属性

一个属性可以使用通用函数 `QObject::property()`和 `QObject::setProperty()`进行读写，除了属性名，无需知晓属性所属类的任何细节。

下面的代码片断中，调用 `QAbstractButton::setDown()`和 `QObject::setProperty()`来设置属性“down”。

```cpp
QPushButton *button = new QPushButton;
QObject *object = button;

button->setDown(true);
object->setProperty("down", true);
```

> 优化建议：
> 通过属性的 `WRITE` 访问属性优于上述两者，因为速度更快并且在编译期间有更好的诊断。
> 但以这种方式设置属性你需要在编译期间了解这个类（能够访问其定义）。

通过名称访问属性，能够让你在编译期间访问不了解的类。你可以在运行时期通过 `QObject`、`QMetaObject` 和 `QMetaProperties` 查询类属性。

```cpp
QObject *object = ...
const QMetaObject *metaobject = object->metaObject();
int count = metaobject->propertyCount();
for (int i=0; i<count; ++i) {
    QMetaProperty metaproperty = metaobject->property(i);
    const char *name = metaproperty.name();
    QVariant value = object->property(name);
    ...
}
```

上面的代码片段中，`QMetaObject::property()`用于获取在未知类中定义的每个属性的 `metadata`。
从 `metadata` 中获取属性名，并传递给 `QObject::property()`来获取当前对象的属性值。

## 一个简单的例子

假设我们有一个类 `MyClass`，它从 `QObject` 派生并且在其 `private` 区域使用了 `Q_OBJECT` 宏。
我们想在 `MyClass` 类中声明一个属性去保持一个 `priority` 值的追踪。
属性名为 `priority`，它是在 `MyClass` 中定义的 `Priority` 枚举类型。

我们在类的 `private` 区域使用 `Q_PROPERTY()`来声明属性。

`READ` 函数名为 `priority`，并且包含一个名为 `setPriority` 的 `WRITE` 函数。

枚举类型必须使用 `Q_ENUM()`宏注册到元对象系统中。

注册一个枚举类型使得枚举器名可以在调用 `QObject::setProperty()`时使用。
我们还必须为 `READ` 和 `WRITE` 函数提供我们自己的声明。

`MyClass` 的声明看起来如下：

```cpp
class MyClass : public QObject
{

    Q_PROPERTY(Priority priority READ priority WRITE setPriority NOTIFY priorityChanged)

public:
    MyClass(QObject *parent = nullptr);
    ~MyClass();

    enum Priority
    {
        High,
        Low,
        VeryHigh,
        VeryLow
    };
    Q_ENUM(Priority)

    void setPriority(Priority priority) {
        m_priority = priority;
        emit priorityChanged(priority);
    }
    Priority priority() const { return m_priority; }
signals:
    void priorityChanged(Priority);

private:
    Q_OBJECT
    Priority m_priority;
};
```

`READ` 函数是 `const` 的并返回属性类型。`WRITE` 函数返回 `void` 并有一个属性类型的参数。元对象编译器强制做这些事情。

给定一个指向 `MyClass` 实例的指针，或一个指向 `QObject` 的指针（该指针是 `MyClass` 的实例），有两种方式设置 `priority` 属性：

```cpp
MyClass *myinstance = new MyClass;
QObject *object = myinstance;

myinstance->setPriority(MyClass::VeryHigh);
object->setProperty("priority", "VeryHigh");
```

在此例子中，声明在 `MyClass` 中的枚举类型是属性的类型，并使用 `Q_ENUM()`宏注册在元对象系统中。这使得枚举值可以在调用 `setProperty()`时做为字符串使用。如果枚举类型在其它类中声明，那么需要使用枚举的全名（如：`OtherClass::Priority`)，且此类也必须从 QObject 派生，且使用 `Q_ENUM()`宏注册枚举类型。

像 `Q_ENUMS()`宏一样，类似的宏 Q_FLAG()也是可用的，它注册一个枚举类型，但是它把枚举类型作为一个 `flags` 集合，也就是，值可以用 OR 操作来合并。
一个 I/O 类可能具有枚举值 Read 和 Write 并且 `QObject::setProperty()`可以接受 `Read | Write`。应使用 `Q_FLAGS()`来注册此枚举类型。

## 动态属性

QObject::setProperty()也可以用来在运行时期向一个类的实例添加新的属性。

- 当使用一个名称和值调用此函数时，如果 `QObject` 中一个给定名称的属性已存在，并且如果给定的值与属性的类型兼容，则值就存储到属性中，并返回 true。如果值与属性类型不兼容，属性值则不会改变，并返回 false。
- 但是如果 QObject 中一个给定名称的属性不存在（如：并没用 `Q_PROPERTY()`声明），则一个带有给定名称和值的新属性就被自动添加到 QObject 中，**但是依然会返回 false**。这意味着返回 false 不能用于确定一个属性是否被真的被设置了，除非你预先知道这个属性已经存在于 QObject 中。

> 注意：
> 动态属性是在每一个实例的基础上添加的，也就是，它们被添加到 `QObject` 中，而不是 `QMetaObject`。
> 可以通过传递一个属性名和一个无效的 `QVariant` 到 `QObject::setProperty()`从一个实例中移除属性。默认的 `QVariant` 构造器会构造一个无效的 `QVariant`。
> 动态属性可用 `QObject::property()`来查询，就像在编译期使用 `Q_PROPERTY()`声明的属性一样。

## 属性和自定义类型

通过属性使用的自定义类型需要使用 `Q_DECLARE_METATYPE()`宏注册，以便它们的值能被保存在 `QVariant` 对象中。
这使得它们适用于在类定义中使用 `Q_PROPERTY()`宏声明的静态属性，以及运行时创建的动态属性。

## 为类添加附加信息

与属性系统相连接的是一个附加宏, `Q_CLASSINFO()`。用于添加额外的 `name-value` 对到类的元对象中。例如：

```cpp
Q_CLASSINFO("Version", "3.0.0")
```

和其它 `meta-data` 一样，类信息可以在运行时通过 `meta-object` 访问，详情见 `QMetaObject::classInfo()` 。

也可参考 `Meta-Object System`, `Signals and Slots`, `Q_DECLARE_METATYPE()`, `QMetaType`, `QVariant`

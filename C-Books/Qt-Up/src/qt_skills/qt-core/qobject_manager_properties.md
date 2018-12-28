# Qt 对象动态增加属性

Dynamic Properties

> `QObject::setProperty()` can also be used to add new properties to an instance of a class at runtime. When it is called with a name and a value, if a property with the given name exists in the QObject, and if the given value is compatible with the property's type, the value is stored in the property, and true is returned. If the value is not compatible with the property's type, the property is not changed, and false is returned. But if the property with the given name doesn't exist in the QObject (i.e., if it wasn't declared with `Q_PROPERTY()`), a new property with the given name and value is automatically added to the QObject, but false is still returned. This means that a return of false can't be used to determine whether a particular property was actually set, unless you know in advance that the property already exists in the QObject.

> Note that dynamic properties are added on a per instance basis, i.e., they are added to QObject, not QMetaObject. A property can be removed from an instance by passing the property name and an invalid QVariant value to `QObject::setProperty()`. The default constructor for QVariant constructs an invalid QVariant.

> Dynamic properties can be queried with `QObject::property()`, just like properties declared at compile time with `Q_PROPERTY()`.

- `QObject::setProperty()`
- `QObject::property()`

示例代码：

```cpp
MyClass *myinstance = new MyClass;
QObject *object = myinstance;

myinstance->setPriority(MyClass::VeryHigh);
object->setProperty("priority", "VeryHigh");
```

# 获取类 ClassInfo 信息

## 调用文件要加入如下代码

```cpp
#include <QMetaClassInfo>
```

## 获取 QMetaClassInfo 的信息

```cpp
const QMetaObject* metaObject = this->metaObject();

std::cout << "metaObject->className() = " << metaObject->className() << std::endl;

std::cout << "metaObj->classInfo : = " << std::endl;
for(int i = metaObject->classInfoOffset(); i < metaObject->classInfoCount(); ++i) {
    std::cout << metaObject->classInfo(i).name() << std::endl;
}
std::cout << "----------------------"  << std::endl;
```

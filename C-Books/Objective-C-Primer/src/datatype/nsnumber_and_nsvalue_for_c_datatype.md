# NSNumber 和 NSValue 对基础 C 数据类型的对象化封装

由于 Objective-C 中常用的数据容器，如 NSArray，NSDictionary 等，只能处理 Objective-C 中的对象级别的数据类型，对于 C 中的很多数据类型，如 int，float 等，无法直接处理。针对这个问题，Objective-C 提供了两种存储数据的对象 NSNumber 和 NSValue，能将 C 中的基本数据类型，包括数值型和结构体型的数据转化成 Objective-C 可以处理的对象。

NSNumber 和 NSValue 都能将 C 中的基本数据类型转化成 Objective-C 中的对象。

## C 中的基本数据类型 <> NSValue

### 1. C 中的基本数据类型转换成 NSValue

```cpp
NSValue *value = [NSValue valueWithBytes:&result objCType:@encode(int)];
// 其中，result是基本数据的值，int是我们要转化的基本数据类型
```

### 2. NSValue 转化成 C 中的基本数据类型

```cpp
[value getValue:&result];
// 其中，value是一个NSValue类型的对象，result是一个已知的类型的基本数据类型。经过这样的转化，NSValue中保存的数值就放到了result中了
```

## C 中的基本数据类型 <> NSNumber

NSNumber 是 NSValue 的子类，它的出现我理解的就是更加方便了除结构体以外的 C 中的基本数据类型和 Objective-C 中对象的相互转化，NSNumber 本身提供了很多类方法和实例方法，可以完成这些操作。

### 1. C 中的基本数据类型转换成 NSNumber

```cpp
NSNumber    *number = [NSNumber numberWithInt:3];
```

### 2. NSNumber 转换层 C 中的基本数据类型

```cpp
NSInteger   result = [number integerValue];
```

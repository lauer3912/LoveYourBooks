# NSString 为何要用 COPY 属性

copy 属性将制造一个传入对象的副本并且将指针指向这个新副本。

```h
@property (copy) NSString *lastName;
```

此时生成的 setter 方法应该是:

```cpp
- (void)setLastName:(NSString *)d
{
 lastName = [d copy];
}
```

类似这样:

```cpp
// Create a mutable string
NSMutableString *x = [[NSMutableString alloc] initWithString:@"Ono"];
// Pass it to setLastName:
[myObj setLastName:x];
// 'copy' prevents this from changing the lastName
[x appendString:@" Lennon"];
```

此时你将 x 传给 setLastName：方法后，lastName 指向的对象并不是 x，而是 x 的副本，此时 x 属性发生改变并不会对 lastName 造成影响，是一种切断关联的拷贝方式。copy 保证了内容不会意外改变。

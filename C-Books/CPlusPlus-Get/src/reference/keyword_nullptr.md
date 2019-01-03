# C++11 关键字 nullptr 的作用

C++11 中，nullptr 是空指针，可用来给（任意对象类型的）指针赋值。

广义整型 `(integral types) = char, short, int, long, long long and their unsigned counterparts, and bool, wchar_t, char16_t, and char32_`

## 调用重载函数更明确

C++ 中，0 首先被视为 int 型，而 NULL 首先被视为广义整型 (integral types)，至于具体是 int，long 或是其它，要视相应的情况而定

下面三个函数，因为形参类型的不同，构成重载函数。如果各传递三个不同的实参，来选择调用哪个函数，则会出现如下问题：

```cpp
// three overloads of f
void f(int);
void f(bool);
void f(void*);

f(0);       // calls f(int), not f(void*)
f(NULL);    // might not compile, but typically calls f(int). Never calls f(void*)
f(nullptr); // calls f(void*) overload
```

- 1. C++ 视 0 首先为 int 型，因此，调用 f(0) 即调用 f(int)
- 2. NULL 的情况复杂些，C++ 首先视其为广义整型。假如 NULL 被定义为普通的 0，则调用 f(int)；
  - 如果 NULL 被定义成 0L，则 long -> int, long -> bool, 0L -> void\*, 这三种情况都是合法的，此时，编译器会报错
- 3. 使用 nullptr，则不会有重载函数调用模糊的问题
  - nullptr 不属于广义整型，也不是普通意义上的指针。
  - nullptr 的实际类型是 std::nullptr_t，它能够隐式的转换成所有的原始指针类型，故可将其视为一个可指向所有类型的指针。

## 让代码更清晰

使用 nullptr 代替 0 或 NULL，能显著提高代码的清晰度，尤其是和 auto 连用时，如下：

```cpp
auto result = findRecord( /* arguments */ );
if (result == 0) {
    ...
}

auto result = findRecord( /* arguments */ );
if (result == nullptr) {
    ...
}
```

使用 0 与 result 作比较，则一时不能确定 findRecord 的返回值类型 (可能是广义整型，也可能是指针类型); 使用 nullptr，可以清楚地知道 findRecord 的返回值，必定是一个指针类型.

## 应用到模板函数更明显

当程序中有模板 (template) 时， nullptr 的好处更加明显：

```cpp
// call these only when the appropriate mutex is locked
int f1(std::shared_ptr<Widget> spw);
double f2(std::unique_ptr<Widget> upw);
bool f3(Widget* pw);

// calling code that wants to pass null pointers
std::mutex f1m, f2m, f3m; // mutexes for f1, f2, and f3
using MuxGuard = std::lock_guard<std::mutex>;

...
{
    MuxGuard g(f1m);        // lock mutex for f1
    auto result = f1(0);    // pass 0 as null ptr to f1
}                           // unlock mutex

...
{
    MuxGuard g(f2m);        // lock mutex for f2
    auto result = f2(NULL); // pass NULL as null ptr to f2
}                           // unlock mutex

...
{
    MuxGuard g(f3m);            // lock mutex for f3
    auto result = f3(nullptr);  // pass nullptr as null ptr to f3
}                  　　　　　　　 // unlock mutex
```

lock mutex -> call function -> unlock mutex，这个模式在程序中重复了三次，要想避免这种重复，可用一个模板函数代替

```cpp
template<typename FuncType, typename MuxType, typename PtrType>
auto lockAndCall(FuncType func, MuxType& mutex, PtrType ptr) -> decltype(func(ptr))  // C++11
{
    MuxGuard g(mutex);
    return func(ptr);
}
```

最后，调用该模板函数.

```cpp
auto result1 = lockAndCall(f1, f1m, 0);          // error!
...
auto result2 = lockAndCall(f2, f2m, NULL);       // error!
...
auto result3 = lockAndCall(f3, f3m, nullptr);    // fine
```

当 0 作为实参传递给 lockAndCall 函数时，其被 C++ 推断为 int 型，这与 f1 所期望的 std::shared_ptr<Widget> 型参数明显不符，因此出现报错。

同理，NULL 与 f2 期望的 std::unique_ptr<Widget> 型参数也不符合。

nullptr，作为 ptr 传给 f1 或 f2 时，被推断为 std::nullptr_t ； 作为 ptr 传给 f3 时，std::nullptr_t 会隐式的转换成 Widget\*，确保了参数类型的一致

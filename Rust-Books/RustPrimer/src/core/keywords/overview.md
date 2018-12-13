# 关键字

The following list contains keywords that are reserved for current or future use by the `Rust` language.
As such, they cannot be used as identifiers (except as raw identifiers), including names of `functions`, `variables`, `parameters`, `struct fields`, `modules`, `crates`, `constants`, `macros`, `static values`, `attributes`, `types`, `traits`, or `lifetimes`. 

下面的列表包含 Rust 中正在使用或者以后会用到的关键字。因此，这些关键字不能被用作标识符（除了 [原始标识符][raw-identifiers]），这包括函数、变量、参数、结构体字段、模块、crate、常量、宏、静态值、属性、类型、trait 或生命周期
的名字。

1. **abstract** -
2. **as** - perform primitive casting, disambiguate the specific trait containing an item, or rename items in use and extern crate statements. 强制原生类型转换，消除特定包含项的 trait 的歧义，或者对 `use` 和 `extern crate` 语句中的项重命名
3. **async** -
4. **become** -
5. **box** -
6. **break** - exit a loop immediately. 立刻退出或跳出循环
7. **const** - define constant items or constant raw pointers. 定义常量或不变裸指针（constant raw pointer）
8. **continue** - continue to the next loop iteration. 继续进入下一次循环迭代
9. **crate** - link an external crate or a macro variable representing the crate in which the macro is defined. 链接（link）一个外部 **crate** 或一个代表宏定义的 **crate** 的宏变量
10. **do** -
11. **dyn** - dynamic dispatch to a trait object. 动态分发 trait 对象
12. **else** - fallback for if and if let control flow constructs. 作为 `if` 和 `if let` 控制流结构的 fallback
13. **enum** - define an enumeration. 定义一个枚举
14. **extern** - link an external crate, function, or variable. 链接一个外部 **crate** 、函数或变量
15. **false** - Boolean false literal. 布尔字面值 `false`
16. **final** -
17. **fn** - define a function or the function pointer type. 定义一个函数或 **函数指针类型** (*function pointer type*)
18. **for** - loop over items from an iterator, implement a trait, or specify a higher-ranked lifetime. 遍历一个迭代器或实现一个 trait 或者指定一个更高级的生命周期
19. **if** - branch based on the result of a conditional expression. 基于条件表达式的结果分支
20. **impl** - implement inherent or trait functionality. 实现自有或 trait 功能
21. **in** - part of for loop syntax. `for` 循环语法的一部分
22. **let** - bind a variable. 绑定一个变量
23. **loop** - loop unconditionally. 无条件循环
24. **macro** - macro 宏
25. **match** - match a value to patterns. 模式匹配
26. **mod** - define a module. 定义一个模块
27. **move** - make a closure take ownership of all its captures. 使闭包获取其所捕获项的所有权
28. **mut** - denote mutability in references, raw pointers, or pattern bindings. 表示引用、裸指针或模式绑定的可变性性
29. **override** -
30. **priv** -
31. **pub** - denote public visibility in struct fields, impl blocks, or modules. 表示结构体字段、`impl` 块或模块的公有可见性
32. **ref** - bind by reference. 通过引用绑定
33. **return** - return from function. 从函数中返回
34. **Self** - a type alias for the type implementing a trait. 实现 trait 的类型的类型别名
35. **self** - method subject or current module. 表示方法本身或当前模块
36. **static** - global variable or lifetime lasting the entire program execution. 表示全局变量或在整个程序执行期间保持其生命周期
37. **struct** - define a structure. 定义一个结构体
38. **super** - parent module of the current module. 表示当前模块的父模块
39. **trait** - define a trait.  定义一个 trait
40. **true** - Boolean true literal. 布尔字面值 `true`
41. **try** -
42. **type** - 定义一个类型别名或关联类型
43. **typeof** -
44. **unsafe** - denote unsafe code, functions, traits, or implementations. 表示不安全的代码、函数、trait 或实现
45. **unsized** -
46. **use** - bring symbols into scope. 引入外部空间的符号
47. **virtual** -
48. **where** - denote clauses that constrain a type. 表示一个约束类型的从句
49. **while** - loop conditionally based on the result of an expression. 基于一个表达式的结果判断是否进行循环
50. **yield** -

## 原始标识符 Raw identifiers

Raw identifiers let you use keywords where they would not normally be allowed by prefixing them with *r#*.

原始标识符（Raw identifiers）允许你使用通常不能使用的关键字，其带有 `r#` 前缀。

例如，`match` 是关键字。如果尝试编译这个函数：

```rust,ignore
fn match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

会得到这个错误：

```text
error: expected identifier, found keyword `match`
 --> src/main.rs:4:4
  |
4 | fn match(needle: &str, haystack: &str) -> bool {
  |    ^^^^^ expected identifier, found keyword
```

可以通过原始标识符编写：

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

注意 `r#` 前缀需同时用于函数名和调用。

## 动机

出于一些原因这个功能是实用的，不过其主要动机是解决跨版本问题。比如，`try` 在 2015 edition 中不是关键字，而在 2018 edition 则是。所以如果如果用 2015 edition 编写的库中带有 `try` 函数，在 2018 edition 中调用时就需要使用原始标识符。

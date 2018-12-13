# Macro

## 简介

学过 C 语言的人都知道 `#define` 用来定义宏(macro)，而且大学很多老师都告诉你尽量少用宏，因为 C 里面的宏是一个很危险的东西-宏仅仅是简单的文本替换，完全不管语法，类型，非常容易出错。听说过或用过 Lisp 的人觉得宏极其强大，就连美国最大的创业孵化器公司创始人 Paul Gram 也极力鼓吹 Lisp 的宏是有多么强大。那么宏究竟是什么样的东西呢？这一章通过 Rust 的宏系统带你揭开宏(Macro)的神秘面纱。

Rust 中的宏几乎无处不在，其实你写的第一个 Rust 程序里面就已经用到了宏，对，就是那个有名的 hello-world。`println!("Hello, world!")` 这句看起来很像函数调用，但是在"函数名"后面加上了感叹号，这个是专门用来区分普通函数调用和宏调用的。另外从形式上看，与函数调用的另一个区别是参数可以用圆括号(`()`)、花括号(`{}`)、方括号(`[]`)中的任意一种括起来，比如这行也可以写成 `println!["Hello, world!"]` 或 `println!{"Hello, world!"}`，不过对于 Rust 内置的宏都有约定俗成的括号，比如 `vec!` 用方括号，`assert_eq!` 用圆括号。

我们已经在本书中像 *println!* 这样使用过宏了，但还没完全探索什么是宏以及它是如何工作的。

既然宏看起来与普通函数非常像，那么使用宏有什么好处呢？是否可以用函数取代宏呢？答案显然是否定的，首先 Rust 的函数不能接受任意多个参数，其次函数是不能操作语法单元的，即把语法元素作为参数进行操作，从而生成代码，例如 `mod`, `crate` 这些是 Rust 内置的关键词，是不可能直接用函数去操作这些的，而宏就有这个能力。

* 什么是宏以及与函数有何区别
* 如何定义一个声明式宏（ declarative macro ）来进行元编程（metaprogramming）
* 如何定义一个过程式宏（ procedural macro ）来自定义 `derive` traits

### 宏和函数的区别

从根本上来说，宏是一种为写其他代码而写代码的方式，即所谓的*元编程*。例如，*元编程*中使用的 `derive` 属性，其用来方便生成各种 trait 的实现。我们也在本书中使用过 `println!` 宏和 `vec!` 宏。所有的这些宏 *扩展开* 来以生成比你手写更多的代码。

> 要记住：相比函数，宏是用来生成代码的，在调用宏的地方，编译器会先将宏进行展开，生成代码，然后再编译展开后的代码。

元编程对于减少大量编写和维护的代码是非常有用的，它也扮演了函数的角色。但宏有一些函数所没有的附加能力。

一个函数标签必须声明函数参数个数和类型。而宏只接受一个可变参数：用一个参数调用 `println!("hello")` 或用两个参数调用 `println!("hello {}", name)` 。而且，宏可以在编译器翻译代码前展开，例如，宏可以在一个给定类型上实现 trait 。因为函数是在运行时被调用，同时 trait 需要在运行时实现，所以函数无法像宏这样。

实现一个宏而不是函数的消极面是宏定义要比函数定义更复杂，因为你正在为写 Rust 代码而写代码。由于这样的间接性，宏定义通常要比函数定义更难阅读、理解以及维护。

宏和函数的另一个区别是：宏定义无法像函数定义那样出现在模块命名空间中。当使用外部包（ external crate ）时，为了防止无法预料的名字冲突，在导入外部包的同时也必须明确地用 `#[macro_use]` 注解将宏导入到项目中。下面的例子将所有定义在 `serde` 包中的宏导入到当前包中：

```rust,ignore
#[macro_use]
extern crate serde;
```

如果 `extern crate` 能够将宏默认导入而无需使用明确的注解，则会阻止你使用同时定义相同宏名的两个包。在练习中，这样的冲突并不经常遇到，但使用的包越多，越有可能遇到。

宏和函数最重要的区别是：在一个文件中，必须在调用宏`之前`定义或导入宏，然而却可以在任意地方定义或调用函数。

宏定义格式是： `macro_rules! macro_name { macro_body }`，其中 `macro_body` 与模式匹配很像， `pattern => do_something` ，所以 Rust 的宏又称为 Macro by example (基于例子的宏)。其中 `pattern` 和 `do_something` 都是用配对的括号括起来的，括号可以是圆括号、方括号、花括号中的任意一种。匹配可以有多个分支，每个分支以分号结束。

还是先来个简单的例子说明

```rust
macro_rules! create_function {
    ($func_name:ident) => (
        fn $func_name() {
            println!("function {:?} is called", stringify!($func_name))
        }
    )
}

fn main() {
    create_function!(foo);
	foo();
}

```

上面这个简单的例子是用来创建函数，生成的函数可以像普通函数一样调用，这个函数可以打印自己的名字。编译器在看到 `create_function!(foo)` 时会从前面去找一个叫 `create_function` 的宏定义，找到之后，就会尝试将参数 `foo` 代入 `macro_body`，对每一条模式按顺序进行匹配，只要有一个匹配上，就会将 `=>` 左边定义的参数代入右边进行替换，如果替换不成功，编译器就会报错而不会往下继续匹配，替换成功就会将右边替换后的代码放在宏调用的地方。这个例子中只有一个模式，即 `$func_name:ident`，表示匹配一个标识符，如果匹配上就把这个标识符赋值给 `$func_name`，宏定义里面的变量都是以 `$` 开头的，相应的类型也是以冒号分隔说明，这里 `ident` 是变量 `$func_name` 的类型，表示这个变量是一个 `identifier`，这是语法层面的类型(designator)，而普通的类型如 `char, &str, i32, f64` 这些是语义层面的类型。在 `main` 函数中传给宏调用 `create_function` 的参数 `foo` 正好是一个标识符(`ident`)，所以能匹配上，`$func_name` 就等于 `foo`，然后把 `$func_name` 的值代入 `=>` 右边，成了下面这样的

```rust
fn foo() {
    println!("function {:?} is called", stringify!(foo))
}
```

所以最后编译器编译的实际代码是

```rust
fn main() {
    fn foo() {
	    println!("function {:?} is called", stringify!(foo))
	}
	foo();
}
```

上面定义了 `create_function` 这个宏之后，就可以随便用来生成函数了，比如调用 `create_function!(bar)` 就得到了一个名为 `bar` 的函数

通过上面这个例子，大家对宏应该有一个大致的了解了。下面就具体谈谈宏的各个组成部分。

## 宏的结构

### 宏名

宏名字的解析与函数略微有些不同，宏的定义必须出现在宏调用之前，即与 C 里面的函数类似--函数定义或声明必须在函数调用之前，只不过 Rust 宏没有单纯的声明，所以宏在调用之前需要先定义，而 Rust 函数则可以定义在函数调用后面。宏调用与宏定义顺序相关性包括从其它模块中引入的宏，所以引入其它模块中的宏时要特别小心，这个稍后会详细讨论。

下面这个例子宏定义在宏调用后面，编译器会报错说找不到宏定义，而函数则没问题

```rust
fn main() {
    let a = 42;
    foo(a);
	bar!(a);
}

fn foo(x: i32) {
	println!("The argument you passed to function is {}", x);
}

macro_rules! bar {
	($x:ident) => { println!("The argument you passed to macro is {}", $x); }
}
```

上面例子中把宏定义挪到 `main` 函数之前或者 `main` 函数里面 `bar!(a)` 调用上面，就可以正常编译运行。

宏调用虽然与函数调用很像，但是宏的名字与函数名字是处于不同命名空间的，之所以提出来是因为在有些编程语言里面宏和函数是在同一个命名空间之下的。看过下面的例子就会明白

```rust
fn foo(x: i32) -> i32 {
    x * x
}

macro_rules! foo {
    ($x:ident) => { println!("{:?}", $x); }
}
fn main() {
    let a = 5;
	foo!(a);
    println!("{}", foo(a));
}
```

### 指示符(designator)

宏里面的变量都是以 `$` 开头的，其余的都是按字面去匹配，以 `$` 开头的变量都是用来表示语法(syntactic)元素，为了限定匹配什么类型的语法元素，需要用指示符(designator)加以限定，就跟普通的变量绑定一样用冒号将变量和类型分开，当前宏支持以下几种指示符：

* ident: 标识符，用来表示函数或变量名
* expr: 表达式
* block: 代码块，用花括号包起来的多个语句
* pat: 模式，普通模式匹配（非宏本身的模式）中的模式，例如 `Some(t)`, `(3, 'a', _)`
* path: 路径，注意这里不是操作系统中的文件路径，而是用双冒号分隔的限定名(qualified name)，如 `std::cmp::PartialOrd`
* tt: 单个语法树
* ty: 类型，语义层面的类型，如 `i32`, `char`
* item: 条目，
* meta: 元条目
* stmt: 单条语句，如 `let a = 42;`

加上这些类型限定后，宏在进行匹配时才不会漫无目的的乱匹配，例如在要求标识符的地方是不允许出现表达式的，否则编译器就会报错。而 C/C++ 语言中的宏则仅仅是简单的文本替换，没有语法层面的考虑，所以非常容易出错。

### 重复(repetition)

宏相比函数一个很大的不同是宏可以接受任意多个参数，例如 `println!` 和 `vec!`。这是怎么做到的呢？

没错，就是重复(repetition)。模式的重复不是通过程序里面的循环(for/while)去控制的，而是指定了两个特殊符号 `+` 和 `*`，类似于正则表达式，因为正则表达式也是不关心具体匹配对象是一个人名还是一个国家名。与正则表达式一样， `+` 表示一次或多次（至少一次），而 `*` 表示零次或多次。重复的模式需要用括号括起来，外面再加上 `$`，例如 `$(...)*`, `$(...)+`。需要说明的是这里的括号和宏里面其它地方一样都可以是三种括号中的任意一种，因为括号在这里仅仅是用来标记一个模式的开始和结束，大部分情况重复的模式是用逗号或分号分隔的，所以你会经常看到 `$(...),*`, `$(...);*`, `$(...),+`, `$(...);+` 这样的用来表示重复。

还是来看一个例子

```rust
macro_rules! vector {
	($($x:expr),*) => {
		{
			let mut temp_vec = Vec::new();
			$(temp_vec.push($x);)*
			temp_vec
		}
	};
}

fn main() {
	let a = vector![1, 2, 4, 8];
	println!("{:?}", a);
}
```

这个例子初看起来比较复杂，我们来分析一下。

首先看 `=>` 左边，最外层是圆括号，前面说过这个括号可以是圆括号、方括号、花括号中的任意一种，只要是配对的就行。然后再看括号里面 `$(...),*` 正是刚才提到的重复模式，重复的模式是用逗号分隔的，重复的内容是 `$x:expr`，即可以匹配零次或多次用逗号分隔的表达式，例如 `vector![]` 和 `vector![3, x*x, s-t]` 都可以匹配成功。

接着看 `=>` 右边，最外层也是一个括号，末尾是分号表示这个分支结束。里面是花括号包起来的代码块，最后一行没有分号，说明这个 macro 的值是一个表达式，`temp_vec` 作为表达式的值返回。第一条语句就是普通的用 `Vec::new()` 生成一个空 vector，然后绑定到可变的变量 `temp_vec` 上面，第二句比较特殊，跟 `=>` 左边差不多，也是用来表示重复的模式，而且是跟左边是一一对应的，即左边匹配到一个表达式(`expr`)，这里就会将匹配到的表达式用在 `temp_vec.push($x);` 里面，所以 `vector![3, x*x, s-t]` 调用就会展开成

```rust
{
	let mut temp_vec = Vec::new();
	temp_vec.push(3);
	temp_vec.push(x*x);
	temp_vec.push(s-t);
	temp_vec
}
```

看着很复杂的宏，细细分析下来是不是很简单，不要被这些符号干扰了

### 递归(recursion)

除了重复之外，宏还支持递归，即在宏定义时调用其自身，类似于递归函数。因为rust的宏本身是一种模式匹配，而模式匹配里面包含递归则是函数式语言里面最常见的写法了，有函数式编程经验的对这个应该很熟悉。下面看一个简单的例子：

```rust
macro_rules! find_min {
    ($x:expr) => ($x);
    ($x:expr, $($y:expr),+) => (
        std::cmp::min($x, find_min!($($y),+))
    )
}

fn main() {
    println!("{}", find_min!(1u32));
    println!("{}", find_min!(1u32 + 2 , 2u32));
    println!("{}", find_min!(5u32, 2u32 * 3, 4u32));
}
```

因为模式匹配是按分支顺序匹配的，一旦匹配成功就不会再往下进行匹配（即使后面也能匹配上），所以模式匹配中的递归都是在第一个分支里写最简单情况，越往下包含的情况越多。这里也是一样，第一个分支 `($x:expr)` 只匹配一个表达式，第二个分支匹配两个或两个以上表达式，注意加号表示匹配一个或多个，然后里面是用标准库中的 `min` 比较两个数的大小，第一个表达式和剩余表达式中最小的一个，其中剩余表达式中最小的一个是递归调用 `find_min!` 宏，与递归函数一样，每次递归都是从上往下匹配，只到匹配到基本情况。我们来写写 `find_min!(5u32, 2u32 * 3, 4u32)` 宏展开过程

1. `std::cmp::min(5u32, find_min!(2u32 * 3, 4u32))`
2. `std::cmp::min(5u32, std::cmp::min(2u32 * 3, find_min!(4u32)))`
3. `std::cmp::min(5u32, std::cmp::min(2u32 * 3, 4u32))`

分析起来与递归函数一样，也比较简单。

### 卫生(hygienic Macro)

有了重复和递归，组合起来就是一个很强大的武器，可以解决很多普通函数无法抽象的东西。但是这里面会有一个安全问题，也是 C/C++ 里面宏最容易出错的地方，不过 Rust 像 Scheme 一样引入了卫生(Hygiene)宏，有效地避免了这类问题的发生。

C/C++ 里面的宏仅仅是简单的文本替换，下面的 C 经过宏预处理后，宏外面定义的变量 `a` 就会与里面定义的混在一起，从而按作用域 shadow 外层的定义，这会导致一些非常诡异的问题，不去看宏具体定义仔细分析的话，很难发现这类 bug。这样的宏是不卫生的，不过也有些奇葩的 Hacker 觉得这是一个非常棒的特性，例如 CommanLisp 语言里面的宏本身很强大，但不是卫生的，而某些 Hacker 还以这个为傲，搞一些奇技淫巧故意制造出这样的 shadow 行为实现一些很 fancy 的效果。这里不做过多评论，对 C 比较熟悉的同学可以分析一下下面这段代码运行结果与第一印象是否一样。

```c
#define INCI(i) {int a=0; ++i;}
int main(void)
{
    int a = 0, b = 0;
    INCI(a);
    INCI(b);
    printf("a is now %d, b is now %d\n", a, b);
    return 0;
}
```

卫生宏最开始是由 Scheme 语言引入的，后来好多语言基本都采用卫生宏，即编译器或运行时会保证宏里面定义的变量或函数不会与外面的冲突，在宏里面以普通方式定义的变量作用域不会跑到宏外面。

```rust
macro_rules! foo {
    () => (let x = 3);
}

macro_rules! bar {
    ($v:ident) => (let $v = 3);
}

fn main() {
    foo!();
    println!("{}", x);
	bar!(a);
	println!("{}", a);
}
```

上面代码中宏 `foo!` 里面的变量 `x` 是按普通方式定义的，所以其作用域限定在宏里面，宏调用结束后再引用 `x` 编译器就会报错。要想让宏里面定义的变量在宏调用结束后仍然有效，需要按 `bar!` 里面那样定义。不过对于 `item` 规则就有些不同，例如函数在宏里面以普通方式定义后，宏调用之后，这个函数依然可用，下面代码就可以正常编译。

```rust
macro_rules! foo {
    () => (fn x() { });
}

fn main() {
    foo!();
    x();
}
```

## 导入导出(import/export)

前面提到宏名是按顺序解析的，所以从其它模块中导入宏时与导入函数、trait 的方式不太一样，宏导入导出用 `#[macro_use]` 和 `#[macro_export]`。父模块中定义的宏对其下的子模块是可见的，要想子模块中定义的宏在其后面的父模块中可用，需要使用 `#[macro_use]`。

```rust
macro_rules! m1 { () => (()) }

// 宏 m1 在这里可用

mod foo {
    // 宏 m1 在这里可用

    #[macro_export]
    macro_rules! m2 { () => (()) }

    // 宏 m1 和 m2 在这里可用
}

// 宏 m1 在这里可用
#[macro_export]
macro_rules! m3 { () => (()) }

// 宏 m1 和 m3 在这里可用

#[macro_use]
mod bar {
    // 宏 m1 和 m3 在这里可用

    macro_rules! m4 { () => (()) }

    // 宏 m1, m3, m4 在这里均可用
}

// 宏 m1, m3, m4 均可用
```

crate 之间只有被标为 `#[macro_export]` 的宏可以被其它 crate 导入。假设上面例子是 `foo` crate 中的部分代码，则只有 `m2` 和 `m3` 可以被其它 crate 导入。导入方式是在 `extern crate foo;` 前面加上 `#[macro_use]`

```rust
#[macro_use]
extern crate foo;
// foo 中 m2, m3 都被导入
```

如果只想导入 `foo` crate 中某个宏，比如 `m3`，就给 `#[macro_use]` 加上参数
```rust
#[macro_use(m3)]
extern crate foo;
// foo 中只有 m3 被导入
```

## 调试

虽然宏功能很强大，但是调试起来要比普通代码困难，因为编译器默认情况下给出的提示都是对宏展开之后的，而不是你写的原程序，要想在编译器错误与原程序之间建立联系比较困难，因为这要求你大脑能够人肉编译展开宏代码。不过还好编译器为我们提供了 `--pretty=expanded` 选项，能让我们看到展开后的代码，通过这个展开后的代码，往上靠就与你自己写的原程序有个直接对应关系，往下靠与编译器给出的错误也是直接对应关系。

目前将宏展开需要使用 unstable option，通过 `rustc -Z unstable-options --pretty=expanded hello.rs` 可以查看宏展开后的代码，如果是使用的 cargo 则通过 `cargo rustc -- -Z unstable-options --pretty=expanded` 将项目里面的宏都展开。不过目前是没法只展开部分宏的，而且由于 hygiene 的原因，会对宏里面的名字做些特殊的处理(mangle)，所以程序里面的宏全部展开后代码的可读性比较差，不过依然比依靠大脑展开靠谱。

下面可以看看最简单的 hello-word 程序里面的 `println!("Hello, world!")` 展开结果，为了 hygiene 这里内部临时变量用了 `__STATIC_FMTSTR` 这样的名字以避免名字冲突，即使这简单的一句展开后看起来也还是不那么直观的，具体这里就不详细分析了。

```
$ rustc -Z unstable-options --pretty expanded hello.rs
#![feature(prelude_import)]
#![no_std]
#[prelude_import]
use std::prelude::v1::*;
#[macro_use]
extern crate std as std;
fn main() {
    ::std::io::_print(::std::fmt::Arguments::new_v1({
                                                        static __STATIC_FMTSTR:
                                                               &'static [&'static str]
                                                               =
                                                            &["Hello, world!\n"];
                                                        __STATIC_FMTSTR
                                                    },
                                                    &match () { () => [], }));
}
```

---

## 以下内容做为补充内容

### 通用元编程的声明式宏 `macro_rules!`

在 Rust 中，最广泛使用的宏形式是 *declarative macros* 。通常也指 *macros by example* 、*`macro_rules!` macros* 或简单的 *macros* 。在其核心中，声明式宏使你可以写一些和 Rust 的 `match` 表达式类似的代码。正如在第六章讨论的那样，`match` 表达式是控制结构，其接收一个表达式，与表达式的结果进行模式匹配，然后根据模式匹配执行相关代码。宏也将一个值和包含相关代码的模式进行比较；此种情况下，该值是 Rust 源代码传递给宏的常量，而模式则与源代码结构进行比较，同时每个模式的相关代码成为传递给宏的代码<!-- 这部分翻译自己不太满意-->。所有的这些都在编译时发生。

可以使用 `macro_rules!` 来定义宏。让我们通过查看 `vec!` 宏定义来探索如何使用 `macro_rules!` 结构。第八章讲述了如何使用 `vec!` 宏来生成一个给定值的 vector。例如，下面的宏用三个整数创建一个 vector `：

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

也可以使用 `vec!` 宏来构造两个整数的 vector 或五个字符串切片的 vector 。但却无法使用函数做相同的事情，因为我们无法预先知道参数值的数量和类型。

在示例 D-1 中来看一个 `vec!` 稍微简化的定义。 

```rust
#[macro_export]
macro_rules! vec {
    ( $( $x:expr ),* ) => {
        {
            let mut temp_vec = Vec::new();
            $(
                temp_vec.push($x);
            )*
            temp_vec
        }
    };
}
```

<span class="caption">示例 D-1: `vec!` 宏定义的一个简化版本</span>

> 注意：标准库中实际定义的 `vec!` 包括预分配适当量的内存。这部分为代码优化，为了让示例简化，此处并没有包含在内。

无论何时导入定义了宏的包，`#[macro_export]` 注解说明宏应该是可用的。 如果没有 `#[macro_export]` 注解，即使凭借包使用 `#[macro_use]` 注解，该宏也不会导入进来，

接着使用 `macro_rules!` 进行了宏定义，且所定义的宏并*不带*感叹号。名字后跟大括号表示宏定义体，在该例中是 `vec` 。

`vec!` 宏的结构和 `match` 表达式的结构类似。此处有一个单边模式 `( $( $x:expr ),* )` ，后跟 `=>` 以及和模式相关的代码块。如果模式匹配，该相关代码块将被执行。假设这只是这个宏中的模式，且只有一个有效匹配，其他任何匹配都是错误的。更复杂的宏会有多个单边模式。<!-- 此处 arm, one arm 并未找到合适的翻译-->

宏定义中有效模式语法和在第十八章提及的模式语法是不同的，因为宏模式所匹配的是 Rust 代码结构而不是值。回过头来检查下示例 D-1 中模式片段什么意思。对于全部的宏模式语法，请查阅[参考]。

[参考]: https://github.com/rust-lang/book/blob/master/reference/macros.html

首先，一对括号包含了全部模式。接下来是后跟一对括号的美元符号（ `$` ），其通过替代代码捕获了符合括号内模式的值。`$()` 内则是 `$x:expr` ，其匹配 Rust 的任意表达式或给定 `$x` 名字的表达式。

`$()` 之后的逗号说明一个逗号分隔符可以有选择的出现代码之后，这段代码与在 `$()` 中所捕获的代码相匹配。紧随逗号之后的 `*` 说明该模式匹配零个或多个 `*` 之前的任何模式。

当以 `vec![1, 2, 3];` 调用宏时，`$x` 模式与三个表达式 `1`、`2` 和 `3` 进行了三次匹配。

现在让我们来看看这个出现在与此单边模式相关的代码块中的模式：在 `$()*` 部分中所生成的 `temp_vec.push()` 为在匹配到模式中的 `$()` 每一部分而生成。`$x` 由每个与之相匹配的表达式所替换。当以 `vec![1, 2, 3];` 调用该宏时，替换该宏调用所生成的代码会是下面这样：

```rust,ignore
let mut temp_vec = Vec::new();
temp_vec.push(1);
temp_vec.push(2);
temp_vec.push(3);
temp_vec
```

我们已经定义了一个宏，其可以接收任意数量和类型的参数，同时可以生成能够创建包含指定元素的 vector 的代码。


鉴于大多数 Rust 程序员*使用*宏而不是*写*宏，此处不再深入探讨 `macro_rules!` 。请查阅在线文档或其他资源，如 [“The Little Book of Rust Macros”][tlborm] 来更多地了解如何写宏。

[tlborm]: https://danielkeep.github.io/tlborm/book/index.html

### 自定义 `derive` 的过程式宏

第二种形式的宏叫做*过程式宏*（ *procedural macros* ），因为它们更像函数（一种过程类型）。过程式宏接收 Rust 代码作为输入，在这些代码上进行操作，然后产生另一些代码作为输出，而非像声明式宏那样匹配对应模式然后以另一部分代码替换当前代码。在书写部分附录时，只能定义过程式宏来使你在一个通过 `derive` 注解来指定 trait 名的类型上实现 trait 。

我们会创建一个 `hello_macro` 包，该包定义了一个关联到 `hello_macro` 函数并以 `HelloMacro` 为名的trait。并非让包的用户为其每一个类型实现`HelloMacro` trait，我们将会提供一个过程式宏以便用户可以使用 `#[derive(HelloMacro)]` 注解他们的类型来得到 `hello_macro` 函数的默认实现。该函数的默认实现会打印 `Hello, Macro! My name is TypeName!`，其中 `TypeName` 为定义了 trait 的类型名。换言之，我们会创建一个包，让使用该包的程序员能够写类似示例 D-2 中的代码。 

<span class="filename">文件名: src/main.rs</span>

```rust,ignore
extern crate hello_macro;
#[macro_use]
extern crate hello_macro_derive;

use hello_macro::HelloMacro;

#[derive(HelloMacro)]
struct Pancakes;

fn main() {
    Pancakes::hello_macro();
}
```

<span class="caption">示例 D-2: 包用户所写的能够使用过程式宏的代码</span>

运行该代码将会打印 `Hello, Macro! My name is Pancakes!` 第一步是像下面这样新建一个库：

```text
$ cargo new hello_macro --lib
```

接下来，会定义 `HelloMacro` trait 以及其关联函数：

<span class="filename">文件名: src/lib.rs</span>

```rust
pub trait HelloMacro {
    fn hello_macro();
}
```

现在有了一个包含函数的 trait 。此时，包用户可以实现该 trait 以达到其期望的功能，像这样：

```rust,ignore
extern crate hello_macro;

use hello_macro::HelloMacro;

struct Pancakes;

impl HelloMacro for Pancakes {
    fn hello_macro() {
        println!("Hello, Macro! My name is Pancakes!");
    }
}

fn main() {
    Pancakes::hello_macro();
}
```

然而，他们需要为每一个他们想使用 `hello_macro` 的类型编写实现的代码块。我们希望为其节约这些工作。

另外，我们也无法为 `hello_macro` 函数提供一个能够打印实现了该 trait 的类型的名字的默认实现：Rust 没有反射的能力，因此其无法在运行时获取类型名。我们需要一个在运行时生成代码的宏。

下一步是定义过程式宏。在编写该附录时，过程式宏必须在包内。该限制后面可能被取消。构造包和包中宏的惯例如下：对于一个 `foo` 的包来说，一个自定义的派生过程式宏的包被称为 `foo_derive` 。在 `hello_macro` 项目中新建名为 `hello_macro_derive` 的包。

```text
$ cargo new hello_macro_derive --lib
```

由于两个包紧密相关，因此在 `hello_macro` 包的目录下创建过程式宏的包。如果改变在 `hello_macro` 中定义的 trait ，同时也必须改变在 `hello_macro_derive` 中实现的过程式宏。这两个包需要分别发布，编程人员如果使用这些包，则需要同时添加这两个依赖并导入到代码中。我们也可以只用 `hello_macro` 包而将 `hello_macro_derive` 作为一个依赖，并重新导出过程式宏的代码。但我们组织项目的方式使编程人员使用 `hello_macro` 成为可能，即使他们无需 `derive` 的功能。

需要将 `hello_macro_derive` 声明为一个过程式宏的包。同时也需要 `syn` 和 `quote` 包中的功能，正如注释中所说，需要将其加到依赖中。为 `hello_macro_derive` 将下面的代码加入到 *Cargo.toml* 文件中。

<span class="filename">文件名: hello_macro_derive/Cargo.toml</span>

```toml
[lib]
proc-macro = true

[dependencies]
syn = "0.11.11"
quote = "0.3.15"
```
为定义一个过程式宏，请将示例 D-3 中的代码放在 `hello_macro_derive` 包的 *src/lib.rs* 文件里面。注意这段代码在我们添加 `impl_hello_macro` 函数的定义之前是无法编译的。

<span class="filename">文件名: hello_macro_derive/src/lib.rs</span>

```rust,ignore
extern crate proc_macro;
extern crate syn;
#[macro_use]
extern crate quote;

use proc_macro::TokenStream;

#[proc_macro_derive(HelloMacro)]
pub fn hello_macro_derive(input: TokenStream) -> TokenStream {
    // Construct a string representation of the type definition
    let s = input.to_string();

    // Parse the string representation
    let ast = syn::parse_derive_input(&s).unwrap();

    // Build the impl
    let gen = impl_hello_macro(&ast);

    // Return the generated impl
    gen.parse().unwrap()
}
```

<span class="caption">示例 D-3: 大多数过程式宏处理 Rust 代码的代码</span>

注意在 D-3 中分离函数的方式，这将和你几乎所见到或创建的每一个过程式宏都一样，因为这让编写一个过程式宏更加方便。在 `impl_hello_macro` 被调用的地方所选择做的什么依赖于该过程式宏的目的而有所不同。

现在，我们已经介绍了三个包：`proc_macro` 、 [`syn`] 和 [`quote`] 。Rust 自带 `proc_macro`  ，因此无需将其加到 *Cargo.toml* 文件的依赖中。`proc_macro` 可以将 Rust 代码转换为相应的字符串。`syn` 则将字符串中的 Rust 代码解析成为一个可以操作的数据结构。`quote` 则将 `syn` 解析的数据结构反过来传入到 Rust 代码中。这些包让解析我们所要处理的有序 Rust 代码变得更简单：为 Rust 编写整个的解析器并不是一件简单的工作。

[`syn`]: https://crates.io/crates/syn
[`quote`]: https://crates.io/crates/quote

当用户在一个类型上指定 `#[derive(HelloMacro)]` 时，`hello_macro_derive`  函数将会被调用。
原因在于我们已经使用 `proc_macro_derive` 及其指定名称对 `hello_macro_derive` 函数进行了注解：`HelloMacro` ，其匹配到 trait 名，这是大多数过程式宏的方便之处。

该函数首先将来自 `TokenStream` 的 `输入` 转换为一个名为 `to_string` 的 `String` 类型。该 `String` 代表 派生 `HelloMacro` Rust 代码的字符串。在示例 D-2 的例子中，`s` 是 `String` 类型的 `struct Pancakes;` 值，这是因为我们加上了 `#[derive(HelloMacro)]` 注解。

> 注意：编写本附录时，只可以将 `TokenStream` 转换为字符串，将来会提供更丰富的API。

现在需要将 `String` 类型的 Rust 代码 解析为一个数据结构中，随后便可以与之交互并操作该数据结构。这正是 `syn` 所做的。`syn` 中的 `parse_derive_input` 函数以一个 `String` 作为参数并返回一个 表示解析出 Rust 代码的 `DeriveInput` 结构体。 下面的代码 展示了从字符串 `struct Pancakes;` 中解析出来的 `DeriveInput` 结构体的相关部分。

```rust,ignore
DeriveInput {
    // --snip--

    ident: Ident(
        "Pancakes"
    ),
    body: Struct(
        Unit
    )
}
```

该结构体的字段展示了我们解析的 Rust 代码是一个元组结构体，其 `ident` （ identifier，表示名字）为 `Pancakes` 。该结构体里面有更多字段描述了所有有序 Rust 代码，查阅 [`syn`
documentation for `DeriveInput`][syn-docs] 以获取更多信息。

[syn-docs]: https://docs.rs/syn/0.11.11/syn/struct.DeriveInput.html

此时，尚未定义 `impl_hello_macro` 函数，其用于构建所要包含在内的 Rust 新代码。但在定义之前，要注意 `hello_macro_derive` 函数的最后一部分使用了 `quote` 包中的 `parse` 函数，该函数将 `impl_hello_macro` 的输出返回给 `TokenStream` 。所返回的 `TokenStream` 会被加到我们的包用户所写的代码中，因此，当用户编译他们的包时，他们会获取到我们所提供的额外功能。

你也注意到，当调用 `parse_derive_input` 或 `parse` 失败时，我们调用 `unwrap` 来抛出异常。在过程式宏中，有必要错误上抛异常，因为 `proc_macro_derive` 函数必须返回 `TokenStream` 而不是 `Result` ，以此来符合过程式宏的 API 。我们已经选择用 `unwrap` 来简化了这个例子；在生产中的代码里，你应该通过 `panic!` 或 `expect` 来提供关于发生何种错误的更加明确的错误信息。

现在我们有了将注解的 Rust 代码从 `TokenStream` 转换为 `String` 和 `DeriveInput` 实例的代码，让我们来创建在注解类型上实现 `HelloMacro` trait 的代码。

<span class="filename">文件名: hello_macro_derive/src/lib.rs</span>

```rust,ignore
fn impl_hello_macro(ast: &syn::DeriveInput) -> quote::Tokens {
    let name = &ast.ident;
    quote! {
        impl HelloMacro for #name {
            fn hello_macro() {
                println!("Hello, Macro! My name is {}", stringify!(#name));
            }
        }
    }
}
```

我们得到一个包含以 `ast.ident` 作为注解类型名字（标识符）的 `Ident` 结构体实例。示例 D-2 中的代码说明 `name` 会是 `Ident("Pancakes")` 。

`quote!` 宏让我们编写我们想要返回的代码，并可以将其传入进 `quote::Tokens` 。这个宏也提供了一些非常酷的模板机制；我们可以写 `#name` ，然后 `quote!` 会以 名为 `name` 的变量值来替换它。你甚至可以做些与这个正则宏任务类似的重复事情。查阅 [the `quote` crate’s
docs][quote-docs] 来获取详尽的介绍。

[quote-docs]: https://docs.rs/quote

我们期望我们的过程式宏能够为通过 `#name` 获取到的用户注解类型生成 `HelloMacro` trait 的实现。该 trait 的实现有一个函数 `hello_macro` ，其函数体包括了我们期望提供的功能：打印 `Hello, Macro! My name is` 和注解的类型名。

此处所使用的 `stringify!` 为 Rust 内置宏。其接收一个 Rust 表达式，如 `1 + 2` ， 然后在编译时将表达式转换为一个字符串常量，如 `"1 + 2"` 。这与 `format!` 或 `println!` 是不同的，它计算表达式并将结果转换为 `String` 。有一种可能的情况是，所输入的 `#name` 可能是一个需要打印的表达式，因此我们用 `stringify!` 。 `stringify!` 编译时也保留了一份将 `#name` 转换为字符串之后的内存分配。

此时，`cargo build` 应该都能成功编译 `hello_macro` 和 `hello_macro_derive` 。我们将这些 crate 连接到示例 D-2 的代码中来看看过程式宏的行为。在 *projects* 目录下用 `cargo new pancakes` 命令新建一个二进制项目。需要将 `hello_macro` 和 `hello_macro_derive` 作为依赖加到 `pancakes` 包的 *Cargo.toml*  文件中去。如果你正将 `hello_macro` 和 `hello_macro_derive` 的版本发布到 [*https://crates.io/*][crates.io] 上，其应为正规依赖；如果不是，则可以像下面这样将其指定为 `path` 依赖：

[crates.io]: https://crates.io/

```toml
[dependencies]
hello_macro = { path = "../hello_macro" }
hello_macro_derive = { path = "../hello_macro/hello_macro_derive" }
```

把示例 D-2 中的代码放在 *src/main.rs* ，然后执行 `cargo run` ： 其应该打印 `Hello, Macro! My name is Pancakes!` 。从过程式宏中实现的 `HelloMacro` trait 被包括在内，但并不包含 `pancakes` 的包，需要实现它。`#[derive(HelloMacro)]` 添加了该 trait 的实现。<!-- 中间句子翻译不是太好 -->

### 宏的前景

在将来，Rust 仍会扩展声明式宏和过程式宏。Rust会通过 `macro` 使用一个更好的声明式宏系统，以及为较之 `derive` 的更强大的任务增加更多的过程式宏类型。在本书出版时，这些系统仍然在开发中，请查阅 Rust 在线文档以获取最新信息。
# trait 关键字

## trait 与具体类型

使用`trait`定义一个特征：

```rust
trait HasArea {
    fn area(&self) -> f64;
}
```

`trait` 中的函数可以有两种方式：（1）没有函数体；（2）有函数体，被称为默认实现。

一般情况， `trait` 中的函数可以没有函数体，实现代码交给具体实现它的类型去补充，如：

```rust

trait HasArea {
    fn area(&self) -> f64;
}

struct Circle {
    x: f64,
    y: f64,
    radius: f64,
}

impl HasArea for Circle {
    fn area(&self) -> f64 {
        std::f64::consts::PI * (self.radius * self.radius)
    }
}

fn main() {
    let c = Circle {
        x: 0.0f64,
        y: 0.0f64,
        radius: 1.0f64,
    };
    println!("circle c has an area of {}", c.area());
}
```

**注**: `&self`表示的是`area`这个函数会将调用者的借代引用作为参数。

这个程序会输出：

```shell
circle c has an area of 3.141592653589793
```

## trait与泛型

> 我们了解了Rust中trait的定义和使用，接下来我们介绍一下它的使用场景，从中我们可以窥探出接口这特性带来的惊喜

我们知道泛型可以指任意类型，但有时这不是我们想要的，需要给它一些约束。

### 泛型的trait约束

```rust,ignore
use std::fmt::Debug;
fn foo<T: Debug>(s: T) {
    println!("{:?}", s);
}
```

`Debug` 是**Rust**内置的一个 `trait` ，为"{:?}"实现打印内容，函数 `foo` 接受一个泛型作为参数，并且约定其需要实现`Debug`

### 多trait约束

可以使用多个trait对泛型进行约束：

```rust,ignore
use std::fmt::Debug;
fn foo<T: Debug + Clone>(s: T) {
    s.clone();
    println!("{:?}", s);
}
```

> 说明：`<T: Debug + Clone>`中`Debug`和`Clone`使用`+`连接，表示泛型`T`需要同时实现这两个trait。

### where关键字

约束的trait增加后，**代码看起来就变得诡异了**，这时候，需要使用 `where` 从句：

```rust
use std::fmt::Debug;

fn foo<T: Clone, K: Clone + Debug>(x: T, y: K) {
    x.clone();
    y.clone();
    println!("{:?}", y);
}

// where 从句的写法
fn foo<T, K>(x: T, y: K) where T: Clone, K: Clone + Debug {
    x.clone();
    y.clone();
    println!("{:?}", y);
}

// 或者使用下面这种写法
fn foo<T, K>(x: T, y: K)
    where T: Clone,
          K: Clone + Debug {
    x.clone();
    y.clone();
    println!("{:?}", y);
}
```

## trait与内置类型

内置类型如：`i32`, `i64` 等也可以添加trait实现，为其定制一些功能：

```rust
trait HasArea {
    fn area(&self) -> f64;
}

impl HasArea for i32 {
    fn area(&self) -> f64 {
        *self as f64
    }
}

5.area();
```

这样的做法是有限制的。Rust 有一个`“孤儿规则”`：当你为某类型实现某 trait 的时候，必须要求类型或者 trait 至少有一个是在当前 `crate` 中定义的。你不能为第三方的类型实现第三方的 `trait`。

在调用 `trait` 中定义的方法的时候，一定要记得让这个 trait 可被访问。

```rust
let mut f = std::fs::File::open("foo.txt").ok().expect("Couldn’t open foo.txt");
let buf = b"whatever"; //  buf: &[u8; 8]
let result = f.write(buf);
result.unwrap();
```

这里是错误：

```shell
error: type `std::fs::File` does not implement any method in scope named `write`
let result = f.write(buf);
               ^~~~~~~~~~
```

我们需要先use这个Write trait：

```rust
use std::io::Write; // 引用后，你才能使用write方法

let mut f = std::fs::File::open("foo.txt").expect("Couldn’t open foo.txt");
let buf = b"whatever";
let result = f.write(buf);
# result.unwrap(); // ignore the error
```

这样就能无错误地编译了。

## trait 支持泛型定义

```rust
use std::fmt::Debug;

trait Seq<T> {
    fn dummy(&self, _: T) where T: Debug;
}

impl<T> Seq<T> for Vec<T> {
    /* */
    fn dummy(&self, v: T) where T: Debug{
        println!("call dummy ... {:?}", v);
    }
}

let m = Vec::<bool>::new() ;
println!("{:?}", m);
m.dummy(true);

```

`trait Seq<T>` 是支持泛型的`trait`定义

## trait的默认方法

```rust
trait Foo {
    fn is_valid(&self) -> bool;

    fn is_invalid(&self) -> bool { !self.is_valid() }
}
```

`is_invalid`是默认方法，`Foo`的实现者并不要求实现它，如果选择实现它，会覆盖掉它的默认行为。

## trait的继承

```rust
trait IControler {
    fn build(&self) -> bool;
    fn scale(&self, zoom: f32);
}

trait IDisplay {
    fn draw(&self);
}

trait IToolBar : IControler {
    fn switch(&self);
}
```

`trait` 支持继承，例如：上面的代码说明，`IToolBar`的实现者也要同时实现`IControler`：

```rust
struct WinToolBar;

impl IControler for WinToolBar {
    fn build(&self) -> bool {
        println!("call IControler build ... ");
        false
    }

    fn scale(&self, zoom: f32) {
        println!("call IControler scale ... ");
    }
}

impl IToolBar for WinToolBar {
    fn switch(&self) {
        println!("call IToolBar switch ... ");
    }
}

let bar = WinToolBar{};
bar.build();
bar.scale(0.5f32);
bar.switch();

```

**输出结果:**

```shell
call IControler build ...
call IControler scale ...
call IToolBar switch ...
```

`trait` 也可以实现多重继承，如下面的方式：

```rust
trait IToolBar : IControler +  IDisplay{
    fn switch(&self);
}
```

上面的代码说明，`IToolBar`的实现者也要同时实现`IControler` 和 `IDisplay`：

```rust
struct WinToolBar;

impl IControler for WinToolBar {
    fn build(&self) -> bool {
        println!("call IControler build ... ");
        false
    }

    fn scale(&self, zoom: f32) {
        println!("call IControler scale ... ");
    }
}

impl IToolBar for WinToolBar {
    fn switch(&self) {
        println!("call IToolBar switch ... ");
    }
}

impl IDisplay for WinToolBar {
    fn draw(&self) {
        println!("call IDisplay draw ... ");
    }
}

let bar = WinToolBar{};
bar.build();
bar.scale(0.5f32);
bar.switch();
bar.draw();

```

**输出结果:**

```shell
call IControler build ...
call IControler scale ...
call IToolBar switch ...
call IDisplay draw ...
```

`trait`中，比较容易出现问题的是实现的多个trait存在相同名称的方法，这使得实现者调用该名称方法，出现歧义，编译是不允许通过的。那么，如何解决这样的问题呢？ 这就要用到`通用函数调用方法`， 参照下面的代码：

```rust
trait IToolBar : IControler +  IDisplay{
    fn build(&self) -> bool {
        println!("call IToolBar build ... ");
        false
    }
    fn switch(&self);
}

struct WinToolBar;

impl IControler for WinToolBar {
    fn build(&self) -> bool {
        println!("call IControler build ... ");
        false
    }

    fn scale(&self, zoom: f32) {
        println!("call IControler scale ... ");
    }
}

impl IToolBar for WinToolBar {
    fn switch(&self) {
        println!("call IToolBar switch ... ");
    }
}

impl IDisplay for WinToolBar {
    fn draw(&self) {
        println!("call IDisplay draw ... ");
    }
}

let bar = WinToolBar{};
/// 由于IControler中定义了build函数，IToolBar 也定义了build函数，
/// 那么执行 bar.build() 就会得到以下错误
///       |             bar.build();
///       |                 ^^^^^ multiple `build` found
/// 因此，需要完全限定语法，消除歧义, 例如：
/// IToolBar::build(&bar);

IToolBar::build(&bar);
IControler::build(&bar);

bar.scale(0.5f32);
bar.switch();
bar.draw();
```

**注意**： 
`IToolBar::build(&bar)` 和 `IControler::build(&bar)` 的调用方法，
这部分属于 `method syntax ()` 中的内容，原型如下：

```rust
f(&b)
```

当我们用 `method syntax ()` 调用一个方法比如 b.f()，如果 f() 含有 &self，Rust 会自动 borrow b。在本例这种情况下，我们需要传递一个具体的 &b。

## derive属性

**Rust**提供了一个属性`derive`来自动实现一些trait，这样可以避免重复繁琐地实现他们，能被`derive`使用的trait包括：`Clone`, `Copy`, `Debug`, `Default`, `Eq`, `Hash`, `Ord`, `PartialEq`, `PartialOrd`

```rust
#[derive(Debug)]
struct Foo;

fn main() {
    println!("{:?}", Foo);
}
```

## impl Trait

在版本1.26 开始，Rust提供了`impl Trait`的写法，作为和Scala 对等的`既存型别(Existential Type)`的写法。

在下面这个写法中，`fn foo()`将返回一个实现了`Trait`的trait。

```rust
//before
fn foo() -> Box<Trait> {
    // ...
}

//after
fn foo() -> impl Trait {
    // ...
}
```

相较于1.25 版本以前的写法，新的写法会在很多场合中更有利于开发和执行效率。

### impl Trait 的普遍用例

```rust
trait Trait {
    fn method(&self);
}

impl Trait for i32 {
    // implementation goes here
}

impl Trait for f32 {
    // implementation goes here
}
```

利用Box 会意味：即便回传的内容是固定的，但也会使用到动态内存分配。利用`impl Trait` 的写法可以避免便用Box。

```rust
//before
fn foo() -> Box<Trait> {
    Box::new(5) as Box<Trait>
}

//after
fn foo() -> impl Trait {
    5
}
```

### 其他受益的用例

闭包:

```rust
// before
fn foo() -> Box<Fn(i32) -> i32> {
    Box::new(|x| x + 1)
}

// after
fn foo() -> impl Fn(i32) -> i32 {
    |x| x + 1
}
```

传参：

```rust
// before
fn foo<T: Trait>(x: T) {

// after
fn foo(x: impl Trait) {
```

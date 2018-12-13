# trait对象 （trait object）

trait对象在**Rust**中是指，使用 **指针** 封装的 trait，比如 `&SomeTrait` 和 `Box<SomeTrait>`。

如果，你是C或者C++编程爱好者，对于指针，特别是C++概念中的指针，基类指针应该更好理解。

```rust
trait Foo { fn method(&self) -> String; }

impl Foo for u8 { fn method(&self) -> String { format!("u8: {}", *self) } }
impl Foo for String { fn method(&self) -> String { format!("string: {}", *self) } }

fn do_something(x: &Foo) {
    x.method();
}

fn main() {
    let x = "Hello".to_string();
    do_something(&x);
    let y = 8u8;
    do_something(&y);
}
```

`x: &Foo`其中`x`是一个trait对象，这里用指针是因为`x`可以是任意实现`Foo`的类型实例，内存大小并不确定，但指针的大小是固定的。

## trait对象的实现

`&SomeTrait` 类型，和普通的指针类型`&i32`不同。它不仅包括指向真实对象的指针，还包括一个指向虚函数表的指针。

它的内部实现定义，在`std::raw`模块中：

```rust
#[repr(C)]
#[derive(Copy, Clone)]
#[allow(missing_debug_implementations)]
pub struct TraitObject {
    pub data: *mut (),     // 指向实际类型实例的指针
    pub vtable: *mut (),   // 指向实际类型对于该trait的实现的虚函数表
}
```

其中：

- `data` 是一个指向实际类型实例的指针；
- `vtable` 是一个指向实际类型对于该trait的实现的虚函数表：

技术解释：

- `*mut()` 中，我们关注到 `*`, 这部分，涉及**Rust**语言中的 `原始指针` 。*const T 和 *mut T 在 Rust 中被称为“原始指针”。
  这里两种指针，`*const T` 只读指针，`*mut T` 可变指针。只读指针，就是指向的数据不可修改；可变指针，就是指向的数据可以修改；

  ```rust
    let x = 5;
    let raw = &x as *const i32;

    println!("{:?}", raw); // 0x50ebf6f780

    let mut y = 10;
    let raw_mut = &mut y as *mut i32;

    println!("{:?}", raw_mut); // 0x50ebf6f784
    unsafe {
        // *raw_mut 称为 解引用
        println!("raw points at {:?} is {}", raw_mut, *raw_mut); //raw points at 0x50ebf6f784 is 10
        *raw_mut = 50 + *raw_mut;
        println!("raw points at {:?} is {}", raw_mut, *raw_mut); //raw points at 0x50ebf6f784 is 60
    }
  ```

---

`Foo`的虚函数表类型：

```rust
struct FooVtable {
    destructor: fn(*mut ()),
    size: usize,
    align: usize,
    method: fn(*const ()) -> String,
}
```

之前的代码可以解读为：

```rust
// u8:
// 这个函数只会被指向u8的指针调用
fn call_method_on_u8(x: *const ()) -> String {
    let byte: &u8 = unsafe { &*(x as *const u8) };

    byte.method()
}

static Foo_for_u8_vtable: FooVtable = FooVtable {
    destructor: /* compiler magic */,
    size: 1,
    align: 1,

    method: call_method_on_u8 as fn(*const ()) -> String,
};


// String:
// 这个函数只会被指向String的指针调用
fn call_method_on_String(x: *const ()) -> String {
    let string: &String = unsafe { &*(x as *const String) };

    string.method()
}

static Foo_for_String_vtable: FooVtable = FooVtable {
    destructor: /* compiler magic */,
    size: 24,
    align: 8,

    method: call_method_on_String as fn(*const ()) -> String,
};


let a: String = "foo".to_string();
let x: u8 = 1;

// let b: &Foo = &a;
let b = TraitObject {
    // data存储实际值的引用
    data: &a,
    // vtable存储实际类型实现Foo的方法
    vtable: &Foo_for_String_vtable
};

// let y: &Foo = x;
let y = TraitObject {
    data: &x,
    vtable: &Foo_for_u8_vtable
};

// b.method();
(b.vtable.method)(b.data);

// y.method();
(y.vtable.method)(y.data);
```

## 对象安全

并不是所有的trait都能作为trait对象使用的，比如：

```rust
let v = vec![1, 2, 3];
let o = &v as &Clone;
```

会有一个错误：

```text
error: cannot convert to a trait object because trait `core::clone::Clone` is not object-safe [E0038]
let o = &v as &Clone;
        ^~
note: the trait cannot require that `Self : Sized`
let o = &v as &Clone;
        ^~
```

让我来分析一下错误的原因：

```rust
pub trait Clone: Sized {
    fn clone(&self) -> Self;

    fn clone_from(&mut self, source: &Self) { ... }
}
```

虽然`Clone`本身继承了`Sized`这个trait，但是它的方法`fn clone(&self) -> Self`和`fn clone_from(&mut self, source: &Self) { ... }`含有`Self`类型，而在使用trait对象方法的时候**Rust**是动态派发的，我们根本不知道这个trait对象的实际类型，它可以是任何一个实现了该trait的类型的值，所以`Self`在这里的大小不是`Self: Sized`的，这样的情况在**Rust**中被称为`object-unsafe`或者`not object-safe`，这样的trait是不能成为trait对象的。

总结：

如果一个`trait`方法是`object safe`的，它需要满足：

* 方法有`Self: Sized`约束， 或者
* 同时满足以下所有条件：
  * 没有泛型参数
  * 不是静态函数
  * 除了`self`之外的其它参数和返回值不能使用`Self`类型

如果一个`trait`是`object-safe`的，它需要满足：

* 所有的方法都是`object-safe`的，并且
* trait 不要求 `Self: Sized` 约束

参考[stackoverflow](http://stackoverflow.com/questions/29985153/trait-object-is-not-object-safe-error)
[object safe rfc](https://github.com/rust-lang/rfcs/blob/master/text/0255-object-safety.md)

# **引用&借用（References&Borrowing）**

例子：

```rust
fn main() {
    let mut x: String = String::from("abc");
    {
        let mut some_closure = |c: char| x.push(c);
        some_closure('d');
    }
    println!("x={:?}", x);  //成功打印：x="abcd"
}
```

我们只是去掉了`move` 关键字，去掉`move` 关键字后，**闭包包体内** 就会对 `x` 进行了**可变借用**，而不是“剥夺”`x`的所有权，细心的同学还注意到我们在前后还加了`{}`大括号作用域，是为了作用域结束后让**可变借用**失效，这样`println`才可以成功访问并打印我们期待的内容。

---

如上所示，`Owership` 让我们改变一个变量的值变得“复杂”，那能否像其他编程语言那样随意改变变量的值呢？

答案是有的。

**所有权系统**允许我们通过`“Borrowing”`的方式达到这个目的。
这个机制非常像其他编程语言中的“读写锁”，即同一时刻，只能拥有一个“写锁”，或只能拥有多个“读锁”，不允许“写锁”和“读锁”在同一时刻同时出现。当然这也是数据读写过程中保障一致性的典型做法。只不过Rust是在编译中完成这个(Borrowing)检查的，而不是在运行时，这也就是为什么其他语言程序在运行过程中，容易出现死锁或者野指针的问题。

通过 `&` 符号完成`Borrowing`：

在继续说明之前，我们先把上面的例子做几个大胆尝试。可能，会让你大吃一惊。

1. 代码

    ```rust ,does_not_compile
    fn main() {
        let mut x: String = String::from("abc");
        let mut some_closure = |c: char| &x.push(c);
        some_closure('E');
        println!("x={:?}", x); // BIG PROBLEM
    }
    ```

1. 代码

    ```rust ,does_not_compile
    fn main() {
        let mut x: String = String::from("abc");
        let mut some_closure = |c: char| &x.push(c);
        some_closure('E');
        println!("x={:?}", &x); // BIG PROBLEM
    }
    ```

1. 代码

    ```rust ,does_not_compile
    fn main() {
        let mut x: String = String::from("abc");
        let mut some_closure = |c: char| mut &x.push(c);
        some_closure('E');
        println!("x={:?}", x);
    }
    ```

1. 代码

    ```rust ,does_not_compile
    fn main() {
        let mut x: String = String::from("abc");
        let mut some_closure = |c: char| &mut x.push(c);
        some_closure('E');
        println!("x={:?}", x);
    }
    ```

1. 代码

    ```rust ,does_not_compile
    fn main() {
        let mut x: String = String::from("abc");
        let mut some_closure = move |c: char| x.push(c);
        some_closure('F');
        println!("x={:?}", x);
    }
    ```

1. 代码

    ```rust ,does_not_compile
    fn main() {
        let mut x: String = String::from("abc");
        let mut some_closure = move |c: char| &x.push(c);
        some_closure('F');
        println!("x={:?}", x);
    }
    ```

1. 代码

    ```rust ,does_not_compile
    fn main() {
        let mut x: String = String::from("abc");
        let mut some_closure = move |c: char| &x.push(c);
        some_closure('F');
        println!("x={:?}", &x);
    }
    ```

1. 代码

    ```rust ,does_not_compile
    fn main() {
        let mut x: String = String::from("abc");
        let mut some_closure = move |c: char| x.push(c);
        some_closure('F');
        x = String::from("246654");
        println!("x={:?}", x);
    }
    ```

关键要理解：

- 没有`move` 关键字的时候，**闭包包体内** 就会对 `x` 进行了**可变借用**，而不是“剥夺”`x`的所有权。
  
- 有`move`关键字的时候，`x`所绑定的资源，发生了`所有权`移动，转移到了**闭包包体内**，这是作用域的变化，跳出该**闭包包体内**的作用域之外，就无法通过 `x` 获得该资源的所有权。

---

现在，我们继续来说明`“Borrowing”`的方式。

```rust
fn main() {
    let x: Vec<i32> = vec!(1i32, 2, 3);
    let y = &x;
    println!("x={:?}, y={:?}", x, y);
}
```

`Borrowing(&x)` 并不会发生`所有权` moved (移动语义)，所以`println!`可以同时访问x和y。
通过引用，就可以对普通类型完成修改。

```rust
fn main() {
    let mut x: i32 = 100;
    {
        let y: &mut i32 = &mut x;
        *y += 2;
    }
    println!("{}", x);
}
```

## 借用与引用的区别

借用与引用是一种相辅相成的关系，说白了，就是一个意思。若B是对A的引用，也可称之为B借用了A。

很相近对吧，但是借用一词本意为要归还。所以在Rust用引用时，一定要注意应该在何处何时正确的“归回”借用/引用。
最后面的“高级”小节会详细举例。

### 规则

1. 同一时刻，可变变量绑定，最多只有一个可变借用（&mut T）。
2. 同一时刻，不可变变量绑定，可有0个或多个不可变借用（&T）但不能有任何可变借用。
3. 借用在离开作用域后释放。
4. 在可变借用释放前不可访问源变量。

### 可变性

`Borrowing`也分“不可变借用”（默认，`&T`）和“可变借用”（`&mut T`）。

顾名思义，“不可变借用”是只读的，不可更新被引用的内容。

```rust
fn main() {
    let x: Vec<i32> = vec!(1i32, 2, 3);

    //可同时有多个不可变借用
    let y = &x;
    let z = &x;
    let m = &x;

    //ok
    println!("{:?}, {:?}, {:?}, {:?}", x, y, z, m);
}
```

再次强调下，同一时刻只能有一个可变借用(&mut T)，且被借用的变量本身必须有可变性 :

```rust
fn main() {
    // 源变量x为可变性
    let mut x: Vec<i32> = vec!(1i32, 2, 3);

    // 只能有一个可变借用
    let y = &mut x; // ok
    // let z = &mut x; //错误
    y.push(100);

    //ok
    println!("{:?}", y);

    // 错误，可变借用未释放，源变量不可访问
    // println!("{:?}", x);

} //y在此处销毁
```

### 高级例子

下面的复杂例子，进行了详细的注释，即使看不懂也没关系，可以在完成Lifetimes（生命周期）的学习后再仔细思考本例子。

```rust
fn main() {
    let mut x: Vec<i32> = vec!(1i32, 2, 3);

    //更新数组
    //push中对数组进行了可变借用，并在push函数退出时销毁这个借用
    x.push(10);

    // 构建新的作用域
    {
        //可变借用(1)
        let mut y = &mut x; //ok. 不在同一时刻.
        //这个时候，可以理解x 没有任何资源，不能借用、使用
        y.push(100);
        println!("{:?}", y); //打印: [1, 2, 3, 10, 100]

        // println!("{:?}", x); //[err] 因为，资源所有权已经被“可变借用”给了y, 不能再不可变借用给x

        //可变借用(2)，注意：此处是对y的借用，不可再对x进行借用，
        //因为y在此时依然存活。
        let z = &mut y;
        //这个时候，可以理解y 没有任何资源，不能借用、使用
        z.push(1000);

        println!("{:?}", z); //打印: [1, 2, 3, 10, 100, 1000]

        // println!("{:?}", y); //[err] 因为，资源所有权已经被“可变借用”给了z, 不能再不可变借用给x
    } //y和z在此处被销毁，并释放借用, 还给 x


    //访问x正常
    println!("{:?}", x); //打印: [1, 2, 3, 10, 100, 1000]
}

```

### 总结

1. 借用不改变内存的所有者（Owner），借用只是对源内存的临时引用。
2. 在借用周期内，借用方可以读写这块内存，所有者被禁止读写内存；且所有者保证在有“借用”存在的情况下，不会释放或转移内存。
3. 失去所有权的变量不可以被借用（访问）。
4. 在租借期内，内存所有者保证不会释放/转移/可变租借这块内存，但如果是在**非可变租借**的情况下，所有者是允许继续**非可变租借**出去的。
5. 借用周期满后，所有者收回读写权限
6. 借用周期小于被借用者（所有者）的生命周期。

> 备注：
借用周期，指的是借用的有效时间段。

下面是一些实例代码：

```rust
fn main() {
    let mut x: Vec<i32> = vec!(1i32, 2, 3);

    let y = &x;  // 不可变借用给y [ok]
    let z = &x;  // 不可变借用给z [ok]

    println!("{:?}, {:?}, {:?}", x, y, z); // [ok]
}
```

```rust ,does_not_compile
fn main() {
    // x 是内存的所有者(Owner)
    let mut x: Vec<i32> = vec!(1i32, 2, 3);
    let w = &mut x;
    println!("{:?}", w); // [ok]
    println!("{:?}", x); // [err]  因为，资源所有权已经被“可变借用”给了w, 不能再以“不可变”或“可变”借用给x
}
```

```rust ,does_not_compile
fn main() {
    // 源变量x为可变性
    let mut x: Vec<i32> = vec!(1i32, 2, 3);

    // 只能有一个可变借用
    let y = &mut x; // ok
    // let z = &mut x; //错误
    y.push(100);

    //ok
    println!("{:?}", y);

    // 错误，可变借用未释放，源变量不可访问
    println!("{:?}", x);
}
```

```rust ,does_not_compile
fn main() {
    let mut x: Vec<i32> = vec!(1i32, 2, 3);

    let y = &x;  // 不可变借用给y [ok]
    let z = &x;  // 不可变借用给z [ok]

    println!("{:?}, {:?}, {:?}", x, y, z); // [ok]

    let w = &mut x; //[err] x 已经被借用了，同一时刻，就不能再获得x的任何可变借用。
    w.push(100);
}
```

```rust
fn main() {
    let mut x: Vec<i32> = vec!(1i32, 2, 3);

    // 构建新的作用域
    {
        let u = &mut x;  //[ok] x"可变"借用给 ---> 不可变的u
        u.push(991199);  //[ok] 虽然，u 是不可变的，但是u绑定的资源是可变的，因此，可以修改资源内存
        println!("{:?}", u); // [ok]
    }// u 在此处销毁，并释放借用，还给x

    let y = &x;      // x"不可变"借用给 ---> 不可变的y [ok]
    let z = &x;      // x"不可变"借用给 ---> 不可变的z [ok]
    let mut m = &x;  // x"不可变"借用给 ---> 可变得m [ok]

    println!("{:?}, {:?}, {:?}, {:?}", x, y, z, m); // [ok]

    // 构建新的作用域
    {
        //let w = &mut x; //[err]. x 已经被“不可变”借用，就不能再“可变”借用给其他变量
        //let w = &mut y; //[err]  y 是"不可变"变量，所以，不能可变借用给其他变量
        //let w = &mut z; //[err]  z 是“不可变”变量，所以，不能可变借用给其他变量
        //let w = &mut m; // [ok]
        let mut w = &mut m;
        //w.push(100);  // [err], w 借用的真正资源是不可变的, 所以不能修改资源的内存
        println!("{:?}", w); // [ok]

        {
            //let v = &mut m; // m已经被“可变借用”给了w, 不能再以“不可变”或“可变”借用给其他变量
            let v = &w; //[ok]
            let j = &w; //[ok]

            println!("{:?}, {:?}", v, j); // [ok]


            //let k = &mut w; //[err]  w 已经被“不可变”借用，就不能再“可变”借用给其他变量
            let mut h = &w; //[ok]
            println!("{:?}, {:?}, {:?}", v, j, h); // [ok]

            {
                let n = &mut h; //[ok]
                // 或使用
                //let mut g = &mut h;

                //println!("{:?}", h); // [err] h已经被“可变借用”给了w, 不能再以“不可变”或“可变”借用给其他变量

                //let e = &h; //[err] h已经被“可变借用”给了w, 不能再以“不可变”或“可变”借用给其他变量
                //let t = &h; //[err] h已经被“可变借用”给了w, 不能再以“不可变”或“可变”借用给其他变量

                println!("{:?}", n); // [ok]

            }
        }

    } // w 在此处销毁，并释放借用，还给 x

    println!("{:?}, {:?}, {:?}, {:?}", x, y, z, m); // [ok]
}
```

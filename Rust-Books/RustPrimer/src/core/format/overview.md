# 字符串格式化

说起格式化字符串，Rust采取了一种类似Python里面format的用法，其核心组成是5个宏和2个trait：`format!`、`format_arg!`、`print!`、`println!`、`write!`; `Debug`、`Display`。

* 宏：
    1. `format!`
    2. `format_arg!`
    3. `print!`
    4. `println!`
    5. `write!`
* Trait：
    1. `Debug`
    1. `Display`

相信你们在写Rust版本的Hello World的时候用到了`print!`或者`println!`这两个宏，但是其实最核心的是`format!`，前两个宏只不过将`format!`的结果输出到了console而已。

那么，我们来探究一下`format!`这个神奇的宏吧。

在这里呢，列举`format!`的定义是没卵用的，因为太复杂。我只为大家介绍几种典型用法。学会了基本上就能覆盖你平时80%的需求。

首先我们来分析一下format的一个典型调用

```rust
fn main() {
    let s = format!("{1} 是个有着{0:>0width$}KG重，{height:?}cm高的大胖子! [{0}, {1}, {2}, {3}]",
                81, "wayslog", width=4, height=178);
    //# 参数位置说明
    //{0} 表示索引为0的参数，例如：这里是 81
    //{1} 表示索引为1的参数，例如：这里是 "wayslog"
    //{2} 表示索引为2的参数，例如：这里是 4
    //{3} 表示索引为2的参数，例如：这里是 178
    //# key-value参数表达方式
    // width=4
    // height=178
    println!("{}", s);
    //# output
    // wayslog 是个有着0081KG重，178cm高的大胖子! [81, wayslog, 4, 178]
}
```

我们可以看到，`format!`宏调用的时候参数可以是任意类型，而且是可以position(位置索引)参数和key-value参数混合使用的。但是要注意的一点是，key-value的值只能出现在position值之后并且不占position。
例如，例子里你用`$`引用到的绝对不是`width`，而是会报错。
这里面关于参数稍微有一个规则就是，参数类型必须要实现 `std::fmt` mod 下的某些trait。比如我们看到原生类型大部分都实现了`Display`和`Debug`这两个宏，其中整数类型还会额外实现一个`Binary`，等等。

当然了，我们可以通过 `{:type}`的方式去调用这些参数。

比如这样：

```rust
format!("{:b}", 2);
// 调用 `Binary` trait
// Get : 10
format!("{:?}", "Hello");
// 调用 `Debug`
// Get : "Hello"
```

另外请记住：type这个地方为空的话默认调用的是`Display`这个trait。

关于`:`号后面的东西其实还有更多式子，我们从上面的`{0:>0width$}`来分析它。

首先`>`是一个语义，它表示的是生成的字符串向右对齐，于是我们得到了 `0081`这个值。与之相对的还有`<`(向左对齐)和`^`(居中)。

再接下来`0`是一种特殊的填充语法，他表示用0补齐数字的空位，要注意的是，当0作用于负数的时候，比如上面例子中wayslog的体重是-81，那么你最终将得到`-0081`;当然了，什么都不写表示用空格填充啦;在这一位上，还会出现`+`、`#`的语法，使用比较诡异，一般情况下用不上。

最后是一个组合式子`width$`，这里呢，大家很快就能认出来是表示后面key-value值对中的`width=4`。你们没猜错，这个值表示格式化完成后字符串的长度。它可以是一个精确的长度数值，也可以是一个以`$`为结尾的字符串，`$`前面的部分可以写一个key或者一个postion。

最后，你需要额外记住的是，在width和type之间会有一个叫精度的区域（可以省略不写如例子），他们的表示通常是以`.`开始的，比如`.4`表示小数点后四位精度。最让人遭心的是，你仍然可以在这个位置引用参数，只需要和上面width一样，用`.N$`来表示一个position的参数，但是就是不能引用key-value类型的。这一位有一个特殊用法，那就是`.*`，它不表示一个值，而是表示两个值！第一个值表示精确的位数，第二个值表示这个值本身。这是一种很尴尬的用法，而且极度容易匹配到其他参数。因此，我建议在各位能力或者时间不欠缺的时候尽量把格式化表达式用标准的形式写的清楚明白。尤其在面对一个复杂的格式化字符串的时候。

好了好了，说了这么多，估计你也头昏脑涨的了吧，下面来跟我写一下format宏的完整用法。仔细体会并提炼每一个词的意思和位置。

```rust
format_string := <text> [ format <text> ] *
format := '{' [ argument ] [ ':' format_spec ] '}'
argument := integer | identifier

format_spec := [[fill]align][sign]['#'][0][width]['.' precision][type]
fill := character
align := '<' | '^' | '>'
sign := '+' | '-'
width := count
precision := count | '*'
type := identifier | ''
count := parameter | integer
parameter := integer '$'
```
# 类型转换 as 运算符

其实这个并不算运算符，因为他是个单词`as`。

这个就是C语言中各位熟悉的显式类型转换了。

show u the code:

```rust
fn avg(vals: &[f64]) -> f64 {
    let sum: f64 = sum(vals);
    let num: f64 = len(vals) as f64;
    sum / num
}
```
# 例子：绘制没有边框的正方形

---

## iOS

```cpp
CGContextRef context = UIGraphicsGetCurrentContext(); //设置上下文
//画一个方形图形 没有边框
CGContextSetRGBFillColor(context, 0, 0.25, 0, 0.5); //方框的填充色
CGContextFillRect(context, CGRectMake(5, 150, 100, 100)); //画一个方框
```

---

## macOS

```cpp

```

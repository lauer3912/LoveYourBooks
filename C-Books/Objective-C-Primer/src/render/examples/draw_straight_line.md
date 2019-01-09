# 例子：绘制一条直线

---

## iOS

```cpp
CGContextRef context = UIGraphicsGetCurrentContext(); //设置上下文
//画一条线
CGContextSetStrokeColorWithColor(context, [UIColor redColor].CGColor);//线条颜色
CGContextSetLineWidth(context, 5.0);//线条宽度
CGContextMoveToPoint(context, 20, 20); //开始画线, x，y 为开始点的坐标
CGContextAddLineToPoint(context, 300, 20);//画直线, x，y 为线条结束点的坐标
CGContextStrokePath(context); //开始画线
```

---

## macOS

```cpp

```

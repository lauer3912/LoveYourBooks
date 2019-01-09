# 例子：绘制菱形

---

## iOS

```cpp
CGContextRef context5 = UIGraphicsGetCurrentContext(); //设置上下文
//画一个菱形
CGContextSetLineWidth(context, 2.0);
CGContextSetStrokeColorWithColor(context, [UIColor blueColor].CGColor);
CGContextMoveToPoint(context, 100, 100);
CGContextAddLineToPoint(context, 150, 150);
CGContextAddLineToPoint(context, 100, 200);
CGContextAddLineToPoint(context, 50, 150);
CGContextAddLineToPoint(context, 100, 100);
CGContextStrokePath(context);
```

---

## macOS

```cpp

```

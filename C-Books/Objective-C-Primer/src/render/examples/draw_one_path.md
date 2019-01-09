# 例子：绘制一段路径

---

## iOS

```cpp
CGContextRef context5 = UIGraphicsGetCurrentContext(); //设置上下文
//填充了一段路径:
CGContextMoveToPoint(context, 100, 100);
CGContextAddLineToPoint(context, 150, 150);
CGContextAddLineToPoint(context, 100, 200);
CGContextAddLineToPoint(context, 50, 150);
CGContextAddLineToPoint(context, 100, 100);
CGContextSetFillColorWithColor(context, [UIColor redColor].CGColor);
CGContextFillPath(context);
```

---

## macOS

```cpp

```

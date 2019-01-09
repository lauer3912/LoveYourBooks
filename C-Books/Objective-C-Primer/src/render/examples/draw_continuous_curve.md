# 例子：绘制连续曲线

---

## iOS

```cpp
CGContextRef context = UIGraphicsGetCurrentContext(); //设置上下文
 //绘制连续的曲线
CGContextSetLineWidth(context, 5.0);
CGContextSetStrokeColorWithColor(context, [UIColor greenColor].CGColor);
CGContextMoveToPoint(context, 230, 150);//开始画线, x，y 为开始点的坐标
CGContextAddCurveToPoint(context, 310, 100, 300, 200, 220, 220);//画三次点曲线
CGContextAddCurveToPoint(context, 290, 140, 280, 180, 240, 190);//画三次点曲线

CGContextStrokePath(context);//开始画线
```

---

## macOS

```cpp

```

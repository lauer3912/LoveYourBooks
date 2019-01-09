# 例子：绘制连续虚曲线

---

## iOS

```cpp
CGContextRef context = UIGraphicsGetCurrentContext(); //设置上下文
//绘制连续的曲线
CGContextSetLineWidth(context, 5.0);
float dashArray3[] = {3, 2, 10, 20, 5};
CGContextSetLineDash(context, 0, dashArray3, 5);//画虚线
CGContextSetStrokeColorWithColor(context, [UIColor greenColor].CGColor);
CGContextMoveToPoint(context, 5, 400);//开始画线, x，y 为开始点的坐标
CGContextAddCurveToPoint(context, 50, 200, 80, 300, 100, 220);//画三次点曲线
CGContextAddQuadCurveToPoint(context, 150, 100, 200, 200);//画二次点曲线
CGContextAddCurveToPoint(context, 240, 400, 10, 50, 300, 300);//画三次点曲线
CGContextStrokePath(context);//开始画线
```

---

## macOS

```cpp

```

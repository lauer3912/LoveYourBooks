# 例子：绘制虚曲线

---

## iOS

```cpp
CGContextRef context = UIGraphicsGetCurrentContext(); //设置上下文
//绘制虚曲线
CGContextSetRGBStrokeColor(context, 0.3, 0.2, 0.1, 1);//线条颜色
float dashArray2[] = {3, 2, 10};
CGContextSetLineDash(context, 0, dashArray2, 3);//画虚线
CGContextMoveToPoint(context, 5, 90);//开始画线, x，y 为开始点的坐标
CGContextAddCurveToPoint(context, 200, 50, 100, 400, 300, 400);
CGContextStrokePath(context);//开始画线
```

---

## macOS

```cpp

```

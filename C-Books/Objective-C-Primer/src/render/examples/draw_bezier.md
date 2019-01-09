# 例子：绘制贝兹曲线

---

## iOS

```cpp
CGContextRef context = UIGraphicsGetCurrentContext(); //设置上下文
//绘制贝兹曲线
//贝兹曲线是通过移动一个起始点，然后通过两个控制点,还有一个中止点，调用CGContextAddCurveToPoint() 函数绘制
CGContextSetLineWidth(context, 2.0);
CGContextSetStrokeColorWithColor(context, [UIColor blueColor].CGColor);
CGContextMoveToPoint(context, 10, 10);
CGContextAddCurveToPoint(context, 200, 50, 100, 400, 300, 400);
CGContextStrokePath(context);
```

![](render/examples/images/ios_bezier.png)

```cpp
// 画贝塞尔曲线
CGContextRef context = UIGraphicsGetCurrentContext();
CGContextSetRGBStrokeColor(context, 255.0f, 255.0f, 255.0f, 1.0f);
CGContextMoveToPoint(context, 100.0f, 100.0f); // 端点一
CGContextSetLineWidth(context, 2.0f);
// (200, 150) 控制点一 (50, 200) 控制点二 (100,300) 端点二
//CGContextAddCurveToPoint(context, 200, 150, 50, 200, 100, 300); // 三次塞尔曲线
// (200,100) 控制点一 (100,300) 端点二
CGContextAddQuadCurveToPoint(context, 200, 100, 100, 300); // 二次塞尔曲线
CGContextStrokePath(context);
```

---

## macOS

```cpp

```

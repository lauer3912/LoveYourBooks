# 例子：绘制实心矩形和实心圆

---

## iOS

![](render/examples/images/ios_solid_circle_and_solid_rectangle.png)

```cpp
// 实心圆 实心矩形
CGContextRef contextRef = UIGraphicsGetCurrentContext();
CGContextSetRGBStrokeColor(contextRef, 1.0f, 1.0f, 1.0f, 1);
CGContextSetLineWidth(contextRef, 2.0f);
CGFloat components[] = { 1.0f, 0.0f, 0.0f, 1.0f};
CGContextSetFillColor(contextRef, components);
CGContextAddRect(contextRef, CGRectMake(50.0f, 50.0f, 100.0f, 100.0f));
CGContextStrokePath(contextRef);
CGContextFillEllipseInRect(contextRef, CGRectMake(50.0f, 50.0f, 100.0f, 100.0f));
CGContextFillRect(contextRef, CGRectMake(150.0f, 150.0f, 100.0f, 100.0f));
```

---

## macOS

```cpp

```

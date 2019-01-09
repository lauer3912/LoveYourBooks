# 例子：绘制不规则形状

---

## iOS

![](render/examples/images/ios_irregular_shape_01.png)
![](render/examples/images/ios_irregular_shape_02.png)

```cpp
// 画不规则形状
CGContextRef contextRef = UIGraphicsGetCurrentContext();
CGContextSetRGBStrokeColor(contextRef, 1.0f, 1.0f, 1.0f, 1); // 填充时用不到
CGContextSetLineWidth(contextRef, 2.0f); // 填充时用不到
CGFloat components[] = { 1.0f, 0.0f, 0.0f, 1.0f};
CGContextSetFillColor(contextRef, components);
CGContextMoveToPoint(contextRef, 150.0f, 150.0f);
CGContextAddLineToPoint(contextRef, 200.0f, 170.0f);
CGContextAddLineToPoint(contextRef, 180.0f, 300.0f);
CGContextAddLineToPoint(contextRef, 80.0f, 300.0f);
CGContextClosePath(contextRef);
//CGContextFillPath(contextRef); // 填充
CGContextStrokePath(contextRef); // 不填充
```

---

## macOS

```cpp

```

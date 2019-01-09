# 例子：绘制饼图

---

## iOS

![](render/examples/images/ios_pie.png)

```cpp
// 画扇形
// 红色部分
CGContextRef contextRef = UIGraphicsGetCurrentContext();
CGFloat components[] = { 1.0f, 0.0f, 0.0f, 1.0f};
CGContextSetFillColor(contextRef, components);
CGContextMoveToPoint(contextRef, 150.0f, 150.0f);
CGContextAddArc(contextRef, 150.0f, 150.0f, 100.0f, 0 * (M_PI / 180.0f), 120 * (M_PI / 180.0f), 0);
CGContextFillPath(contextRef);
// 绿色部分
CGFloat blueComponents[] = { 0.0f, 1.0f, 0.0f, 1.0f};
CGContextSetFillColor(contextRef, blueComponents);
CGContextMoveToPoint(contextRef, 150.0f, 150.0f);
CGContextAddArc(contextRef, 150.0f, 150.0f, 100.0f, 120 * (M_PI / 180.0f), 200 * (M_PI / 180.0f), 0);
CGContextFillPath(contextRef);
```

---

## macOS

```cpp

```

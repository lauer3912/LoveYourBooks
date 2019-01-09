# 例子：绘制圆角矩形

---

## iOS

```cpp
// 画一个圆角矩形
CGContextRef contextRef = UIGraphicsGetCurrentContext();
CGContextSetRGBStrokeColor(contextRef, 1.0f, 1.0f, 1.0f, 1);
CGContextSetLineWidth(contextRef, 20.0f);
CGContextAddRect(contextRef, CGRectMake(50.0f, 50.0f, 100.0f, 100.0f));
CGContextStrokePath(contextRef);
CGLineJoin lineJoin = kCGLineJoinRound;
CGContextSetLineJoin(contextRef, lineJoin);
CGContextStrokePath(contextRef);
```

---

## macOS

```cpp

```

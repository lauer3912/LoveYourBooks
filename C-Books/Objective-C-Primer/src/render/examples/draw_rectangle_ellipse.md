# 例子：绘制矩形和椭圆

---

## iOS

![](render/examples/images/ios_ectangle_ellipse.png)

```cpp
// 画矩形和圆形(椭圆也是圆哦)
CGContextRef contextRef = UIGraphicsGetCurrentContext();
CGContextSetRGBStrokeColor(contextRef, 1.0f, 1.0f, 1.0f, 1);
CGContextSetLineWidth(contextRef, 2.0f);
CGContextAddRect(contextRef, CGRectMake(50.0f, 50.0f, 200.0f, 100.0f));
CGContextAddEllipseInRect(contextRef, CGRectMake(50.0f, 50.0f, 200.0f, 100.0f));
CGContextStrokePath(contextRef);

// 画圆弧
// CGContextAddArc(contextRef, <#CGFloat x#>, <#CGFloat y#>, <#CGFloat radius#>, <#CGFloat startAngle#>, <#CGFloat endAngle#>, <#int clockwise#>)
// 圆心， 半径， 起始角度， 结束角度， 1，顺时针 0，逆时针
CGContextAddArc(contextRef, 100.0f, 300.0f, 50.0f, 0.0f * ( M_PI/180 ), 90.0f * ( M_PI/180 ), 1);
CGContextStrokePath(contextRef);
```

---

## macOS

```cpp

```

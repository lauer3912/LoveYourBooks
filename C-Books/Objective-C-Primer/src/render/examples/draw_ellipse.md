# 例子：绘制椭圆

---

## iOS

```cpp
CGContextRef context5 = UIGraphicsGetCurrentContext(); //设置上下文
//画椭圆
CGRect aRect= CGRectMake(80, 80, 160, 100);
CGContextSetRGBStrokeColor(context, 0.6, 0.9, 0, 1.0);
CGContextSetLineWidth(context, 3.0);
CGContextAddEllipseInRect(context, aRect); //椭圆, 参数2:椭圆的坐标。
CGContextDrawPath(context, kCGPathStroke);
```

---

## macOS

```cpp

```

# 例子：绘制正方形边框

---

## iOS

```cpp
//画方形边框
CGContextRef context5 = UIGraphicsGetCurrentContext(); //设置上下文
CGContextSetLineWidth(context5, 3.0);
CGContextSetRGBStrokeColor(context5, 0.8, 0.1, 0.8, 1);
CGContextStrokeRect(context5, CGRectMake(5, 5, 300, 400));//画方形边框, 参数2:方形的坐标。
```

---

## macOS

```cpp

```

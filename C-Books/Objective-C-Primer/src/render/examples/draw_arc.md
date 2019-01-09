# 例子：绘制一条弧线

---

## iOS

```cpp
CGContextRef context = UIGraphicsGetCurrentContext(); //设置上下文
//画弧线
CGContextSetRGBStrokeColor(context, 0.3, 0.4, 0.5, 1);//线条颜色
CGContextAddArc(context, 180, 200, 50, 0, 180*(M_PI/180), 0);

CGContextStrokePath(context);//开始画线
```

---

## macOS

```cpp

```

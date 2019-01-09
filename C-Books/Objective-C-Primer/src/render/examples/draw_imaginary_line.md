# 例子：绘制虚线

---

## iOS

```cpp
CGContextRef context = UIGraphicsGetCurrentContext(); //设置上下文
//绘制虚线
CGContextSetRGBStrokeColor(context, 0.1, 0.2, 0.3, 1);//线条颜色
float dashArray1[] = {3, 2};
CGContextSetLineDash(context, 0, dashArray1, 2);//画虚线,可参考http://blog.csdn.net/zhangao0086/article/details/7234859
CGContextMoveToPoint(context, 5, 70);//开始画线, x，y 为开始点的坐标
CGContextAddLineToPoint(context, 310, 70);//画直线, x，y 为线条结束点的坐标
CGContextStrokePath(context);//开始画线
```

---

## macOS

```cpp

```

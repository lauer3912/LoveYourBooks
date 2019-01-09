# CGContextSaveGState 与 CGContextRestoreGState 的作用

使用 `Quartz` 时涉及到一个图形上下文，其中图形上下文中包含一个保存过的图形状态堆栈。在 `Quartz` `创建图形上下文时，该堆栈是空的。CGContextSaveGState` 函数的作用是将当前图形状态推入堆栈。之后，您对图形状态所做的修改会影响随后的描画操作，但不影响存储在堆栈中的拷贝。在修改完成后，您可以通过 `CGContextRestoreGState` 函数把堆栈顶部的状态弹出，返回到之前的图形状态。这种推入和弹出的方式是回到之前图形状态的快速方法，避免逐个撤消所有的状态修改；这也是将某些状态（比如裁剪路径）恢复到原有设置的唯一方式。

```cpp
/// iOS

UIGraphicsBeginImageContextWithOptions(targetRect.size, YES, 0.0);
CGContextRef context = UIGraphicsGetCurrentContext();

float myFillColor[] = {1,0,0,1}; //red;
CGContextSaveGState(context);

CGContextSetRGBFillColor(context, 0,1,1,1);
CGContextFillRect(context, targetRect);
CGContextSetFillColor(context, myFillColor);
CGContextFillEllipseInRect(context, targetRect);
CGContextFillPath(context);
CGContextRestoreGState(context);

UIImage *uiImage = UIGraphicsGetImageFromCurrentImageContext();
UIGraphicsEndImageContext();

```

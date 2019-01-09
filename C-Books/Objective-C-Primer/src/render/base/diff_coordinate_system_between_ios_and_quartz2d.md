# iOS 中 UIKit 坐标系与 Quartz 2D 绘图坐标系的区别

## IOS 中包含 UIKit 坐标系

UIKit 坐标系: X 轴正方向向右,Y 轴正方向向下, 原点在左上角。

### 坐标系的概念

在 iOS 中绘制图形必须在一个二维的坐标系中进行，但在 iOS 系统中存在多个坐标系，常需要处理一些**坐标系的转换**。

先介绍一个图形上下文(graphics context)的概念，比如说我们常用的 CGContext 就是 Quartz 2D 的上下文。
图形上下文包含绘制所需的信息，比如颜色、线宽、字体等。用我们在 Windows 常用的画图来参考，当我们使用画笔 🖌 在白板中写字时，图形上下文就是画笔的属性设置、白板大小、画笔位置等等。

iOS 中，每个图形上下文都会有三种坐标：

1. **绘制坐标系**（也叫**用户坐标系**），我们平时绘制所用的坐标系；
1. **视图（view）坐标系**，固定左上角为原点（0，0）的 view 坐标系；
1. **物理坐标系**，物理屏幕中的坐标系，同样是固定左上角为原点；

![](render/base/images/coordinate_for_ios.png)

根据我们绘制的目标不同（屏幕、位图、PDF 等），会有多个 context；

![](render/base/images/more_graphic_context.png)

**不同 context 的绘制坐标系各不相同**: 比如说 UIKit 的坐标系为左上角原点的坐标系，CoreGraphics 的坐标系为左下角为原点的坐标系。

如下图：

![](render/base/images/coordinate_uikit_and_coregraphics.png)

### CoreGraphics 坐标系和 UIKit 坐标系的转换

CoreText 基于 CoreGraphics，所以坐标系也是 CoreGraphics 的坐标系。

我们回顾下上文提到的两个渲染结果，我们产生如下疑问： UIGraphicsGetCurrentContext 返回的是 CGContext，代表着是左下角为原点的坐标系，用 UILabel（UIKit 坐标系）可以直接 renderInContext，并且“测”字对应为 UILabel 的（0，0）位置，是在左上角？ 当用 CoreText 渲染时，坐标是（0，0），但是渲染的结果是在左上角，并不是在左下角；并且文字是上下颠倒的。 为了探究这个问题，我在代码中加入了一行 log：

```cpp
NSLog(@"CGContext default matrix %@", NSStringFromCGAffineTransform(CGContextGetCTM(context)));

/// 输出结果为: CGContext default matrix [2, 0, 0, -2, 0, 200]
```

CGContextGetCTM 返回是 CGAffineTransform 仿射变换矩阵.

<p>
M =
\begin{vmatrix}
a&b&0\\c&d&0\\tx&ty&1
\end{vmatrix}
<p>

一个二维坐标系上的点 p，可以表达为(x, y, 1)，乘以变换的矩阵，如下

![](render/base/images/transform-formula.png)

把结果相乘，得到下面的关系

![](render/base/images/transform.png)

此时，我们再来看看打印的结果[2, 0, 0, -2, 0, 200]，可以化简为 x' = 2x, y' = 200 - 2y 因为渲染的 view 高度为 100，所以这个坐标转换相当于把原点在左下角（0，100）的坐标系，转换为原点在左上角（0，0）的坐标系！通常我们都会使用 UIKit 进行渲染，所以 iOS 系统在 drawRect 返回 CGContext 的时候，默认帮我们进行了一次变换，以方便开发者直接用 UIKit 坐标系进行渲染。

![](render/base/images/coordinates_uikit_default_convert.png)

我们尝试对系统添加的坐标变换进行还原： 先进行`CGContextTranslateCTM(context, 0, self.bounds.size.height);` 对于`x' = 2x, y' = 200 - 2y`，我们使得`x=x,y=y+100`；（`self.bounds.size.height=100）` 于是有`x' = 2x, y' = 200-2(y+100) = -2y`; 再进行`CGContextScaleCTM(context, 1.0, -1.0)`; 对于`x' = 2x, y' = -2y`，我们使得`x=x, y=-y`; 于是有 `x'=2x, y' = -2(-y) = 2y`

```cpp
- (void)drawRect:(CGRect)rect {
    [super drawRect:rect];
    CGContextRef context = UIGraphicsGetCurrentContext();
    CGContextTranslateCTM(context, 0, self.bounds.size.height);
    CGContextScaleCTM(context, 1.0, -1.0);
    NSLog(@"CGContext default matrix %@", NSStringFromCGAffineTransform(CGContextGetCTM(context)));
    NSAttributedString *attrStr = [[NSAttributedString alloc] initWithString:@"测试文本" attributes:@{
                                                                                                  NSForegroundColorAttributeName:[UIColor whiteColor],
                                                                                                  NSFontAttributeName:[UIFont systemFontOfSize:14],
                                                                                                  }];
    CTFramesetterRef frameSetter = CTFramesetterCreateWithAttributedString((__bridge CFAttributedStringRef) attrStr); // 根据富文本创建排版类CTFramesetterRef
    UIBezierPath * bezierPath = [UIBezierPath bezierPathWithRect:CGRectMake(0, 0, 100, 20)];
    CTFrameRef frameRef = CTFramesetterCreateFrame(frameSetter, CFRangeMake(0, 0), bezierPath.CGPath, NULL); // 创建排版数据
    CTFrameDraw(frameRef, context);
}
```

通过 log 也可以看出来 `CGContext default matrix [2, 0, -0, 2, 0, 0]`； 最终结果如下，文本从**左下角**开始渲染，并且没有出现上下颠倒的情况。

![](render/base/images/coordinates_uikit_draw_example_1.png)

这时我们产生新的困扰： 用 `CoreText` 渲染文字的上下颠倒现象解决，但是修改后的坐标系 `UIKit` 无法正常使用，如何兼容两种坐标系？ iOS 可以使用 `CGContextSaveGState()`方法暂存 context 状态，然后在 `CoreText` 绘制完后通过 `CGContextRestoreGState()`可以恢复 context 的变换。

```cpp
- (void)drawRect:(CGRect)rect {
    [super drawRect:rect];

    CGContextRef context = UIGraphicsGetCurrentContext();
    NSLog(@"CGContext default matrix %@", NSStringFromCGAffineTransform(CGContextGetCTM(context)));
    CGContextSaveGState(context);
    CGContextTranslateCTM(context, 0, self.bounds.size.height);
    CGContextScaleCTM(context, 1.0, -1.0);
    NSAttributedString *attrStr = [[NSAttributedString alloc] initWithString:@"测试文本" attributes:@{
                                                                                                  NSForegroundColorAttributeName:[UIColor whiteColor],
                                                                                                  NSFontAttributeName:[UIFont systemFontOfSize:14],
                                                                                                  }];
    CTFramesetterRef frameSetter = CTFramesetterCreateWithAttributedString((__bridge CFAttributedStringRef) attrStr); // 根据富文本创建排版类CTFramesetterRef
    UIBezierPath * bezierPath = [UIBezierPath bezierPathWithRect:CGRectMake(0, 0, 100, 20)];
    CTFrameRef frameRef = CTFramesetterCreateFrame(frameSetter, CFRangeMake(0, 0), bezierPath.CGPath, NULL); // 创建排版数据
    CTFrameDraw(frameRef, context);
    CGContextRestoreGState(context);


    NSLog(@"CGContext default CTM matrix %@", NSStringFromCGAffineTransform(CGContextGetCTM(context)));
    UILabel *testLabel = [[UILabel alloc] initWithFrame:CGRectMake(0, 0, 100, 20)];
    testLabel.text = @"测试文本";
    testLabel.font = [UIFont systemFontOfSize:14];
    testLabel.textColor = [UIColor whiteColor];
    [testLabel.layer renderInContext:context];
}
```

渲染结果如下，控制台输出的两个 matrix 都是`[2, 0, 0, -2, 0, 200]`；

![](render/base/images/coordinates_uikit_draw_example_2.png)

### 遇到的问题

#### 1. UILabel.layer 在 drawContext 的时候 frame 失效

初始化 UILabel 时设定了 frame，但是没有生效。 `UILabel *testLabel = [[UILabel alloc] initWithFrame:CGRectMake(20, 20, 100, 28)];`这是因为 frame 是在上一层 view 中坐标的偏移，在 renderInContext 中坐标起点与 frame 无关，所以需要修改的是 bounds 属性： `testLabel.layer.bounds = CGRectMake(50, 50, 100, 28);`

#### 2. 在把 UILabel.layer 渲染到 context 的时候，应该采用 drawInContext 还是 renderInContext？

![](render/base/images/renderInContext_drawInContext.png)

虽然这两个方法都可以生效，但是根据画线部分的内容来判断，还是采用了 `renderInContext`，并且问题 1 就是由这里的一句 `Renders in the coordinate space of the layer`，定位到问题所在。

#### 3. 如何理解 CoreGraphics 坐标系不一致后，会出现绘制结果异常？

我的理解方法是，我们可以先不考虑坐标系变换的情况。 如下图，上半部分是普通的渲染结果，可以很容易的想象； 接下来是增加坐标变换后，坐标系变成原点在左上角的顶点，相当于按照下图的虚线进行了一次垂直的翻转。

![](render/base/images/coordinates_uikit_draw_example_3.png)

也可以按照坐标系变换的方式去理解，将左下角原点的坐标系相对 y 轴做一次垂直翻转，然后向上平移 height 的高度，这样得到左上角原点的坐标系。

附录
[Drawing and Printing Guide for iOS Quartz 2D Programming Guide](https://developer.apple.com/library/archive/documentation/GraphicsImaging/Conceptual/drawingwithquartz2d/dq_overview/dq_overview.html)

### iOS 代码示例

#### 1. 把中心点为 A(50,50)长为 20,宽为 10 的矩形以 X 轴逆时针旋转 45 度

```cpp
- (void)drawRect:(CGRect)rect{
  　　/**
  　　 * UIKit坐标系，原点在UIView左上角
   　　*/
  　　CGContextRef context =  UIGraphicsGetCurrentContext();
  　　CGContextSaveGState(context);
  　　CGAffineTransform transform;

  　　/**
  　　 * 变换后 transform = CBA,显然不是想要的结果.
   　　* 这是由于CGAffineTransform变换函数构造的矩阵在左边,如:
   　　* t' = CGAffineTransformTranslate(t,tx,ty)
   　　* 结果为:t' = [ 1 0 0 1 tx ty ] * t
   　　* 累积变换就会得到上面的结果
   　　*/
  　　transform = CGAffineTransformIdentity;
 　　 transform = CGAffineTransformTranslate(transform, -50, -50); //A
  　　transform = CGAffineTransformRotate(transform, M_PI_4);      //B
  　　transform = CGAffineTransformTranslate(transform, 50, 50);   //C

  　　/**
   　　* 为了得到正确结果,调整顺序如下:
   　　*/
  　　transform = CGAffineTransformIdentity;
  　　transform = CGAffineTransformTranslate(transform, 50, 50);    //C
 　　 transform = CGAffineTransformRotate(transform, M_PI_4);       //B
  　　transform = CGAffineTransformTranslate(transform, -50, -50);  //A

 　　 /**
   　　* context函数变换
   　　*/
 　　 //CGContextTranslateCTM(context, 50, 50);    //C
  　　//CGContextRotateCTM(context, M_PI_4);       //B
  　　//CGContextTranslateCTM(context, -50, -50);  //A

  　　CGContextConcatCTM(context, transform);

 　　 /**
  　　 * 绘制矩形
   　　*/
  　　CGContextFillRect(context, CGRectMake(40, 45, 20, 10));

  　　CGContextRestoreGState(context);
}
```

#### 2. 绘制图片

```cpp
void drawImage(CGContextRef context, CGImageRef image , CGRect rect){
 　　 /**
  　　 * 注意变换顺序A->B->C->D
   　　*/
  　　CGContextSaveGState(context);

  　　/**
  　　 * 矩形回到起始位置
   　　*/
  　　CGContextTranslateCTM(context, rect.origin.x, rect.origin.y);  //D

 　　 /**
  　　 * 矩形Y轴正方向平移rect.size.height
  　　 */
  　　CGContextTranslateCTM(context, 0, rect.size.height);           //C

  　　/**
   　　* 垂直反转矩形
   　　*/
 　　 CGContextScaleCTM(context, 1.0, -1.0);                         //B

  　　/**
  　　 * 矩形平移到原点
   　　*/
  　　CGContextTranslateCTM(context, -rect.origin.x, -rect.origin.y);//A

 　　 /**
  　　 * 绘制图片
  　　 */
  　　CGContextDrawImage(context, rect, image);

  　　CGContextRestoreGState(context);
}
```

#### 3. 坐标轴变换

```cpp

/**
 * 原坐标系为Quartz 2D,目标坐标系为UKit,用原坐标系中坐标绘图
 */
- (void)drawRect:(CGRect)rect
{
    //UKit坐标系
    CGContextRef context =  UIGraphicsGetCurrentContext();
    CGContextSaveGState(context);
    CGRect bounds = self.bounds;

    /**
     * 坐标轴变换A->B
     */

    /**
     * 平移坐标轴
     */
    CGContextTranslateCTM(context, 0, bounds.size.height); // B

    /**
     * 翻转Y坐标轴
     */
    CGContextScaleCTM(context, 1, -1);                     //A

    /**
     * 绘制矩形
     */
    CGContextFillRect(context, CGRectMake(10, 10, 20, 20));

    CGContextRestoreGState(context);
}
```

---

## 标准的 Quartz 2D 绘图坐标系

Quartz 2D 绘图坐标系：X 轴正方向向右,Y 轴正方向向上， 原点在左下角。

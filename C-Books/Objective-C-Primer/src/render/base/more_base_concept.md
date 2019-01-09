# 涉及的相关概念和接口

## Quartz

### Quartz 简介

Quartz 是主要的描画接口，支持基于路径的描画、抗锯齿渲染、渐变填充模式、图像、颜色、坐标空间变换、以及 PDF 文档的创建、显示、和分析。

- UIKit 为 Quartz 的图像和颜色操作提供了 Objective-C 的封装。
- Core Animation 为很多 UIKit 的视图属性声明的动画效果提供底层支持，也可以用于实现定制的动画。

Quartz 2D 是 macOS 和 iOS 下的 2d 图形绘制引擎。

---

#### 1. 针对 macOS

---

#### 2. 针对 iOS

在调用您提供的 drawRect:方法之前，视图对象会自动配置其描画环境，使您的代码可以立即进行描画。作为这些配置的一部分，UIView 对象会为当前描画环境创建一个图形上下文（对应于 CGContextRef 封装类型）

用户坐标空间是您发出的所有描画命令的工作环境。该空间的单位由点来表示。设备坐标空间指的是设备内在的坐标空间，由像素来表示。缺省情况下，用户坐标空间上的一个点等于设备坐标空间的一个像素，这意味着一个点等于 1/160 英寸。然而，您不应该假定这个比例总是 1:1。

- UIColor 对象提供了一些便利方法，用于通过 RGB、HSB、和灰度值指定颜色值。
- 您也可以使用 Core Graphics 框架中的 CGContextSetRGBStrokeColor 和 CGContextSetRGBFillColor 函数来创建和设置颜色。
- 路径轮廓可以用像 CGContextStrokePath 这样的函数来画，即用当前的笔划颜色画出以路径为中心位置的线。路径的填充则可以用 CGContextFillPath 函数来实现，它的功能是用当前的填充颜色或样式填充路径线段包围的区域。
- 获取上下文，图形上下文是什么意思？
  CGContextRef context = UIGraphicsGetCurrentContext();

---

## CGContextRef 详解

Graphics Context 是图形上下文,可以将其理解为一块画布,我们可以在上面进行绘画操作,绘制完成后,将画布放到我们的 view 中显示即可,view 看作是一个画框.

Quartz 提供了以下几种类型的 Graphics Context：

1. Bitmap Graphics Context
1. PDF Graphics Context
1. Window Graphics Context
1. Layer Context
1. Post Graphics Context

### 按接口功能分类

#### 1. Managing Graphics Contexts (管理图形上下文)

```Objective-C
CGContextFlush       // 强制所有挂起的绘图操作在一个窗口上下文中立即被渲染到目标设备。
CGContextGetTypeID   // 返回Quartz图形上下文的类型标识符。
CGContextRelease     // 图形上下文的引用计数-1。
CGContextRetain      // 图形上下文的引用计数+1。
CGContextSynchronize // 将一个窗口的图像上下文内容更新，即所有的绘图操作都会在下次同步到窗口上
```

#### 2. Saving and Restoring the Current Graphics State (保存和恢复当前图形状态)

```Objective-C
CGContextSaveGState     // 将当前图形状态的副本PUSH到图形状态栈中；
CGContextRestoreGState  // 将当前图形状态设置为最近一次保存的状态，即恢复状态。
```

需要注意的是，注意,当前绘图环境的所有方面都是图形状态的元素。比如当前路径的图像状态是不考虑的，所以当调用这
个函数的时候是不保存的。保存的图像状态如下：

```Objective-C
/// CTM (current transformation matrix)  /// 变换矩阵
/// clip region
/// image interpolation quality
/// line width
/// line join
/// miter limit
/// line cap
/// line dash
/// flatness
/// should anti-alias
/// rendering intent
/// fill color space
/// stroke color space
/// fill color
/// stroke color
/// alpha value
/// font
/// font size
/// character spacing
/// text drawing mode
/// shadow parameters
/// the pattern phase
/// the font smoothing parameter
/// blend mode
```

#### 3. Getting and Setting Graphics State Parameters (获取和设置图形状态参数)

```Objective-C
CGContextGetInterpolationQuality  /// 返回当前的图形上下文的插值（插值(Interpolation)是在不天生像素的环境下增长图像像素大小的一种方法,在周围像素色彩的根蒂根基上用算术公式计算亡失像素的色彩。）质量水平。
CGContextSetFlatness              /// 设置弯曲的路径中的图形上下文的准确性。
CGContextSetInterpolationQuality  /// 设置图形上下文的插值质量水平。
CGContextSetLineCap               /// 图形环境中的画线的端点的样式设置。
CGContextSetLineDash              /// 设置图形上下文中的虚线的模式。
CGContextSetLineJoin              /// 设置图像上下文中的接接线的样式。
CGContextSetLineWidth             /// 设置图像上下文中的线的宽度。
CGContextSetMiterLimit            /// 设置图像上下文中的连接线的斜接限制。
CGContextSetPatternPhase          /// 设置一个上下文的段落模式。
CGContextSetFillPattern           /// 在指定的图形上下文设置的填充图案模式。
CGContextSetRenderingIntent       /// 在当前图形状态设置渲染意向。
CGContextSetShouldAntialias       /// 设置图形上下文的抗锯齿开启或关闭。
CGContextSetStrokePattern         /// 在指定的图形上下文设置描边图案。
CGContextSetBlendMode
CGContextSetAllowsAntialiasing
CGContextSetAllowsFontSmoothing
CGContextSetShouldSmoothFonts
CGContextSetAllowsFontSubpixelPositioning
CGContextSetShouldSubpixelPositionFonts
CGContextSetAllowsFontSubpixelQuantization
CGContextSetShouldSubpixelQuantizeFonts
```

#### 4. Constructing Paths (构建路径, 用于自定义路径的几何形状)

These functions are used to define the geometry of the current path. For more information on how paths are defined, see CGPath Reference.
这些函数是用来定义路径的几何形状。对于如何定义的路径的更多信息，请参阅 CGPath 参考。

```Objective-C
CGContextAddArc
CGContextAddArcToPoint
CGContextAddCurveToPoint
CGContextAddLines
CGContextAddLineToPoint
CGContextAddPath
CGContextCopyPath
CGContextAddQuadCurveToPoint
CGContextAddRect
CGContextAddRects
CGContextBeginPath
CGContextClosePath
CGContextMoveToPoint
CGContextAddEllipseInRect
```

#### 5. Painting Paths (绘制路径的接口)

These functions are used to stroke along or fill in the current path.
这些功能是用于边缘或填充在当前路径。

```Objective-C
CGContextClearRect
CGContextDrawPath
CGContextEOFillPath
CGContextFillPath
CGContextFillRect
CGContextFillRects
CGContextFillEllipseInRect
CGContextStrokePath
CGContextStrokeRect
CGContextStrokeRectWithWidth
CGContextReplacePathWithStrokedPath
CGContextStrokeEllipseInRect
CGContextStrokeLineSegments
```

#### 6. Getting Information About Paths (获取关于路径的信息)

```Objective-C
CGContextIsPathEmpty            /// 表示目前的路径是否包含任何的子路径。
CGContextGetPathCurrentPoint    /// 返回一个非空的路径中的当前点。
CGContextGetPathBoundingBox     /// 返回包含当前路径的最小矩形。
CGContextPathContainsPoint      /// 检查当前路径中是否包含指定的点。
```

#### 7. Modifying Clipping Paths (修改剪贴剪辑路径)

```Objective-C
CGContextClip                   /// 修改当前剪贴剪辑路径，使用非零绕数规则。
CGContextEOClip                 /// 修改当前剪贴剪辑路径，使用奇偶规则。
CGContextClipToRect
CGContextClipToRects
CGContextGetClipBoundingBox
CGContextClipToMask
```

#### 8. Setting Color, Color Space, and Shadow Values (设置颜色，色彩空间和阴影值)

```Objective-C
CGContextSetAlpha
CGContextSetCMYKFillColor
CGContextSetFillColor
CGContextSetCMYKStrokeColor
CGContextSetFillColorSpace
CGContextSetFillColorWithColor
CGContextSetGrayFillColor
CGContextSetGrayStrokeColor
CGContextSetRGBFillColor
CGContextSetRGBStrokeColor
CGContextSetShadow
CGContextSetShadowWithColor
CGContextSetStrokeColor
CGContextSetStrokeColorSpace
CGContextSetStrokeColorWithColor
```

#### 9. Transforming User Space (转换用户空间)

These functions allow you to examine and change the current transformation matrix (CTM) in a graphics context.
这些功能允许你检查和更改图形上下文的当前转换矩阵（CTM）。

```Objective-C
CGContextConcatCTM
CGContextGetCTM
CGContextRotateCTM
CGContextScaleCTM
CGContextTranslateCTM
```

#### 10. Using Transparency Layers (使用透明图层)

```Objective-C
CGContextBeginTransparencyLayer          /// 开始一个透明层。直到相应的调用CGContextEndTransparencyLayer，在指定范围内的所有后续绘制操作组合到一个完全透明的背景（它被视为一个单独的目标缓冲区从上下文）。调用CGContextEndTransparencyLayer，使用全局alpha和阴影的上下文状态合成到上下文中。
CGContextBeginTransparencyLayerWithRect  /// 开始透明度层，它的边界是指定的矩形，其内容是有界的。
CGContextEndTransparencyLayer            /// 结束一个透明层。
```

#### 11. Drawing an Image to a Graphics Context (绘制图像图形上下文)

```Objective-C
CGContextDrawTiledImage   /// 重复绘制的图像，扩展到提供的矩形，填补当前剪辑区域。
CGContextDrawImage        /// 绘制图像到图形上下文中。
```

#### 12. Drawing PDF Content to a Graphics Context (绘制一个图形上下文的 PDF 内容)

```Objective-C
CGContextDrawPDFPage    /// 绘制一个PDF页面到当前的用户空间。
```

#### 13. Drawing With a Gradient (绘制渐变)

```Objective-C
CGContextDrawLinearGradient  /// 绘制一个渐变填充定义的出发点和落脚点沿线变化。
CGContextDrawRadialGradient  /// 绘制一个沿着由所提供的开始和结束的圆限定的区域变化的渐变填充。
```

#### 14. Drawing With a Shading (绘制底纹/阴影)

```Objective-C
CGContextDrawShading         /// 使用指定的阴影的背景，填充剪切路径。
```

#### 15. Setting Up a Page-Based Graphics Context (建立一个基于页面的图形上下文)

```Objective-C
CGContextBeginPage    /// 基于页面的图形上下文中开始了新的一页。
CGContextEndPage      /// 在基于页面的图形上下文结束当前的页面。
```

#### 16. Drawing Glyphs (绘制字形)

```Objective-C
CGContextShowGlyphs             /// 在当前文本位置显示一个数组的字形。
CGContextShowGlyphsAtPoint      /// 在指定的位置显示一个数组的字形。
CGContextShowGlyphsWithAdvances /// 绘制具有不同的偏移量的一个数组字形。
CGContextShowGlyphsAtPositions  /// 在所提供的位置绘制字形。
```

#### 17. Drawing Text (绘制文本)

```Objective-C
CGContextGetTextMatrix        /// 返回当前文本矩阵。
CGContextGetTextPosition      /// 返回在绘制文本的位置。
CGContextSelectFont           /// 设置在一个图形上下文的字体和字体大小。
CGContextSetCharacterSpacing  /// 设置当前字符间距。
CGContextSetFont              /// 设置上下文的字体。
CGContextSetFontSize          /// 设置上下文的字体大小。
CGContextSetTextDrawingMode   /// 设置当前文本的绘图模式。
CGContextSetTextMatrix        /// 设置当前文本矩阵。
CGContextSetTextPosition      /// 设置要绘制文本的位置。
CGContextShowText             /// 在当前文本位置，由目前的文本矩阵指定的点显示一个字符数组。
CGContextShowTextAtPoint      /// 在指定的位置显示一个字符串。
```

#### 18. Converting Between Device Space and User Space (设备空间和用户空间之间的转换)

```Objective-C
CGContextGetUserSpaceToDeviceSpaceTransform
CGContextConvertPointToDeviceSpace
CGContextConvertPointToUserSpace
CGContextConvertSizeToDeviceSpace
CGContextConvertSizeToUserSpace
CGContextConvertRectToDeviceSpace
CGContextConvertRectToUserSpace
```

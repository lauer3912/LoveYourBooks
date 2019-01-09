# 仿射变换矩阵

## Transform 变换矩阵

### CGAffineTransform: 仿射变换矩阵, 用于 View 的 2D 变换

#### 矩阵的基本知识：

```Objective-C
// 仿射变换矩阵
struct CGAffineTransform
{
  CGFloat a, b, c, d;
  CGFloat tx, ty;
};
```

**应用于二维图形**

```Objective-C
// 构建一个仿射变换矩阵
CGAffineTransform CGAffineTransformMake (CGFloat a,CGFloat b,CGFloat c,CGFloat d,CGFloat tx,CGFloat ty);

// 对于二维图形，存在三个最基本的图形变换操作：（1）平移；（2）缩放；（3）旋转。

// 平移矩阵：创建一个平移的变换
GGAffineTransform CGAffineMakeTranslation(CGFloat tx,CGFloat ty);

// 缩放矩阵：创建一个给定比例缩放的变换
CGAffineTransform CGAffineTransformMakeScale(CGFloat sx, CGFloat sy);

// 旋转矩阵：创建一个旋转角度的变换
CGAffineTransform CGAffineTransformMakeRotation(CGFloat angle);
```

为了把二维图形的变化统一在一个坐标系里，引入了齐次坐标的概念，即把一个图形用一个三维矩阵表示，其中第三列总是(0,0,1)，用来作为坐标系的标准。**所以所有的变化都由前两列完成**.参考下图：

   <p>
   M =
   \begin{vmatrix}
    a&b&0\\c&d&0\\tx&ty&1
   \end{vmatrix}
   <p>

现在介绍`点坐标通过仿射变换后得到新坐标点的`运算原理：

![](render/base/images/transform-formula.png)
![](render/base/images/transform.png)

```text
例如：
（1）一个二维点的坐标可以用一个1*3的矩阵表示，如：[X, Y, 1]; /// {X坐标值，Y坐标值，Z坐标值} 由于是二维的，那么第三列的值，用 1 填充。
（2）按照这样的计算公式计算：[X, Y, 1] * M = [aX + cY + tx, bX + dY + ty, 1];
（3）那么会得到一个新的点 [aX + cY + tx, bX + dY + ty, 1];

```

引用 [通俗的解释仿射变换](https://www.matongxue.com/madocs/244.html)

现在讲讲 `平移`、`缩放` `旋转` 三个矩阵的运算原理。

1.  `平移` , 使用函数 `GGAffineTransform CGAffineMakeTranslation(CGFloat tx,CGFloat ty)`

```text
平移实际上是对矩阵M中的相关参数，设定了以下规则：
（1）a = 1；
（2）d = 1；
（3）b = 0；
（4）c = 0；
所以根据公式：[X, Y, 1] * M = [aX + cY + tx, bX + dY + ty, 1] 计算得到：
新的点坐标等于 [X + tx, Y + ty, 1]; /// {X坐标值，Y坐标值，Z坐标值}
要说明的是tx，ty 是指点坐标按照向量(tx, ty) 进行平移。
例如：tx = -2; ty = 20; 单位是像素。一般说明，点向左平移2个像素，向上平移20个像素。

```

1.  `缩放` , 使用函数 `CGAffineTransform CGAffineTransformMakeScale(CGFloat sx, CGFloat sy)`

```text
缩放实际上是对矩阵M中的相关参数，设定了以下规则：
（1）b = 0；
（2）c = 0；
（3）tx = 0；
（4）ty = 0；
所以根据公式：[X, Y, 1] * M = [aX + cY + tx, bX + dY + ty, 1] 计算得到：
新的点坐标等于 [aX, dY, 1]; /// {X坐标值，Y坐标值，Z坐标值}
要说明的是a是X坐标的缩放系数，d是Y坐标的缩放系数。也就是说X坐标上的点按照a值比例系数缩放，Y坐标上的点按照d值比例系数缩放。
```

1.  `旋转` , 使用函数 `CGAffineTransform CGAffineTransformMakeRotation(CGFloat angle)`

```text
缩放实际上是对矩阵M中的相关参数，设定了以下规则：
（1）a = cosɵ；
（2）b = sinɵ；
（3）c = -sinɵ；
（4）d = cosɵ；
（5）tx = 0；
（6）ty = 0；
所以根据公式：[X, Y, 1] * M = [aX + cY + tx, bX + dY + ty, 1] 计算得到：
新的点坐标等于 [Xcosɵ - Ysinɵ, Xsinɵ + Ycosɵ,  1]; /// {X坐标值，Y坐标值，Z坐标值}
要说明的是ɵ就是旋转的角度，逆时针为正，顺时针为负。
```

#### Transformations 扩展功能

```Objective-C
/// 1.
/// CGAffineTransformTranslate //为一个Transformation(变换)再加上平移
CGAffineTransform CGAffineTransformTranslate (
    CGAffineTransform t,
    CGFloat tx,
    CGFloat ty
);
/// 简单来说就是在变化 t 上在加上平移

/// 2.
/// CGAffineTransformScale    //为一个Transformation(变换)再加上缩放
CGAffineTransform CGAffineTransformScale (
    CGAffineTransform t,
    CGFloat sx,
    CGFloat sy
);

/// 3.
/// CGAffineTransformRotate   //为一个Transformation(变换)再加上旋转
CGAffineTransform CGAffineTransformRotate (
    CGAffineTransform t,
    CGFloat angle
);

/// 4.
/// CGAffineTransformInvert   //返回Transformation(变换)的反转
CGAffineTransform CGAffineTransformInvert (CGAffineTransform t);

/// 5.
/// CGAffineTransformConcat   //合并两个Transformation
CGAffineTransform CGAffineTransformConcat (
    CGAffineTransform t1,
    CGAffineTransform t2)
;
/// 返回一个由 t1 和  t2  合并而成的Transformation
```

#### Transformations 应用

```Objective-C

/// 1.
/// CGPointApplyAffineTransform  //把变化应用到一个点上
CGPoint CGPointApplyAffineTransform (
    CGPoint point,
    CGAffineTransform t
);
// 这个方法的返回值还是一个CGPoint，
// 这个方法最终也只会影响这个点所在的位置

/// 2.
/// CGSizeApplyAffineTransform  //把变化应用到一个区域中
CGSize CGSizeApplyAffineTransform (
    CGSize size,
    CGAffineTransform t
);
// 只会改变区域的大小

/// 3.
/// CGRectApplyAffineTransform  //把变化应用到一个带原点的矩形
CGRect CGRectApplyAffineTransform (
    CGRect rect,
    CGAffineTransform t
);
// 测试三个属性 放缩、旋转和平移都有的一个Transformation ，
// 但处理之后只会改变这个区域原点的位置，和宽、高的大小，并不会旋转


```

#### 检测 Transformation

```Objective-C

// 1.
// CGAffineTransformIsIdentity         // 检测一个Transformation是不是恒等变换，也就是说不变
bool CGAffineTransformIsIdentity ( CGAffineTransform t);    /// 其结果返回一个BOOL值

// 2.
// CGAffineTransformEqualToTransform   // 检测两个Transformation是否相等。
bool CGAffineTransformEqualToTransform (
    CGAffineTransform t1,
    CGAffineTransform t2
);
```

#### 代码示例

##### 1. 图片的缩放旋转

```Objective-C

/// 图片的缩放旋转
- (void)transformImageView{
    CGAffineTransform t = CGAffineTransformMakeScale(scale * previousScale,scale * previousScale);
    t = CGAffineTransformRotate(t, rotation + previousRotation);
    self.imageView.transform = t;
}

/// 1、首先创建了一个变换CGAffineTransform的一个对象 t ，这个变换是用来放缩的，里面的两个参数分别是对宽和高放大或缩小的倍数，这里是以相同比例放缩的。
/// 2、第二行句是在放缩变化中再加入角度的变换。
/// 3、最后把变换赋给图片视图的一个属性transform。
/// 就这么简单就实现了图片的旋转和放缩。

```

##### 2. 水平翻转 与 垂直翻转

```Objective-C
CGAffineTransformMakeScale (CGFloat sx, CGFloat sy);//创建一个给定比例放缩的变换视图引用了这个变换，那么图片的宽度就会变为  width*sx  ，对应高度变为  hight * sy。

CGAffineTransformMakeScale(-1.0, 1.0);//水平翻转
CGAffineTransformMakeScale(1.0,-1.0);//垂直翻转

```

##### 3. 角度旋转 与 弧度旋转

```Objective-C
CGAffineTransform CGAffineTransformMakeRotation ( CGFloat angle); //创建一个旋转角度的变化
在这里可以看到参数并不是一个角度，但是它是把参数作为一个弧度，
然后把弧度再转换为角度来处理，其结果就可能是将一个图片视图旋转了多少度。

```

##### 4. 创建一个平移的变化

```Objective-C
//创建一个平移的变化
CGAffineTransform CGAffineTransformMakeTranslation (CGFloat tx,CGFloat ty);
这个就比较好理解了，假设是一个视图，那么它的起始位置 x 会加上tx , y 会加上 ty
```

### CATransform3D: 主要用于 Layer，为 3D 变换使用

### CGAffineTransform 与 CATransform3D 相互转换

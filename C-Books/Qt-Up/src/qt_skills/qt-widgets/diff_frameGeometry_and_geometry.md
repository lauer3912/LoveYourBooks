# QWidget 的 frameGeometry 与 geometry 有什么区别？

想解决这个问题，一定要了解 QWidget 的几何属性。

如下图所示：

![](qt_skills/qt-widgets/images/qwidget_geometry.jpg)

- frameGeometry，frameSize，x，y，pos：框架的几何区域和大小，框架指窗口的最外层。
- geometry，width，height，size，rect：内部绘图区域的几何框架。

在 WidgetProperty 的构造函数中添加代码

```cpp
WidgetProperty::WidgetProperty(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::WidgetProperty)
{
    ui->setupUi(this);
    setGeometry(0, 0, 400, 300);
}
```

运行代码，窗口的绘图区域左上角和屏幕的左上角刚好吻合，而标题栏都跑到了屏幕外面。

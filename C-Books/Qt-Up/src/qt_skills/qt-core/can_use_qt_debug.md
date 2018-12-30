# 不包含头文件，可以直接使用 qDebug()?

一般的，每次我们使用 qDebug()<<时，都会要求包含头文件 QDebug。如果你是用习惯了 C 语言中的格式化输出，那么也可以像下面的做法来输出打印信息。

```cpp
#include <QObject>
int main(int argc, char *argv[])
{
int num = 20;
char str[20]="hello world";
qDebug("如果只写在括号里，是不需要 QDebug 头文件的 %d %s", num, str);
}
```

实际 qDebug 是包含在 qlongging.h 中的，因为我们的 Qt 程序，一般都会包含 QObject，所以这里的头文件包含了 QObject，从而我们就不必要额外的再添加 QDebug 头文件。

以上对于只打印字符串等一些临时性的基本类型信息时，使用这种方法是非常有效的，但是，要记住 Qt 所支持的基本类型是不可以打印的。

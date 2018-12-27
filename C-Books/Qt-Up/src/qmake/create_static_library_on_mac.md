# MacOS 如何使用 Qt 创建静态库?

## 使用 Qt Creator 创建静态 library, 我们得到最初的`pro`文件

`/code-src/for_mac/static_link_library/matrix/matrixref/matrixref.pro`

```qt.pro
#-------------------------------------------------
#
# Project created by QtCreator 2018-12-26T15:05:13
#
#-------------------------------------------------

# 仅依赖QtCore
QT       -= gui

TARGET = matrixref
TEMPLATE = lib
CONFIG += staticlib

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
        matrixref.cpp

HEADERS += \
        matrixref.h
unix {
    target.path = /usr/lib
    INSTALLS += target
}

```

## 使用 Qt Creator 创建一个控制台, 我们得到最初的`pro`文件

`/code-src/for_mac/static_link_library/matrix/matrxref_console/matrxref_console.pro`

```pro
QT -= gui

CONFIG += c++11 console
CONFIG -= app_bundle

# The following define makes your compiler emit warnings if you use
# any Qt feature that has been marked deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
        main.cpp

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

```

## 修改 `matrxref_console.pro` 文件，增加外部库的引用说明

修改 `/code-src/for_mac/static_link_library/matrix/matrxref_console/matrxref_console.pro` 文件

增加如下代码：

```pro
# 使用外部库
macx{
    LIBS += -L$$PWD/../build-matrixref-Desktop_Qt_5_12_0_clang_64bit2-Debug/ -lmatrixref
    INCLUDEPATH += $$PWD/../matrixref
    DEPENDPATH += $$PWD/../matrixref
    PRE_TARGETDEPS += $$PWD/../build-matrixref-Desktop_Qt_5_12_0_clang_64bit2-Debug/libmatrixref.a
}
```

## 看看源码的调用

发现几个有意思的问题：
（1）Mac 版本的静态库 matrixref 没有显示定义任何一个导出函数，不知道 Windows 版本上如何？

```C++
#if defined __cplusplus
    #include <iostream>
#endif

#include <QCoreApplication>
#include "matrixref.h" // 引用静态库的头文件

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    TechiDaily::Matrixref ref;

#if defined __cplusplus
    std::cout << ref.hi() << std::endl;
#endif

    return a.exec();
}
```

# (Windows)创建动态库?

![](qmake/images/win-create-dynamic-library-01.jpg)
![](qmake/images/win-create-dynamic-library-02.jpg)
![](qmake/images/win-create-dynamic-library-03.jpg)
![](qmake/images/win-create-dynamic-library-04.jpg)
![](qmake/images/win-create-dynamic-library-05.jpg)

## 使用Qt Creator 创建Windows 的动态库

查看 `code-src\for_win\dynamic_link_library\ExtendBest\ExtendBestRef\ExtendBestRef.pro` 文件内容

```pro
#-------------------------------------------------
#
# Project created by QtCreator 2018-12-27T15:36:51
#
#-------------------------------------------------

QT       -= gui

TARGET = ExtendBestRef
TEMPLATE = lib

DEFINES += EXTENDBESTREF_LIBRARY

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
        extendbestref.cpp

HEADERS += \
        extendbestref.h \
        extendbestref_global.h 

unix {
    target.path = /usr/lib
    INSTALLS += target
}

```

## 动态库源码部分

1. `extendbestref_global.h`

    ```h
    #ifndef EXTENDBESTREF_GLOBAL_H
    #define EXTENDBESTREF_GLOBAL_H

    #include <QtCore/qglobal.h>

    #if defined(EXTENDBESTREF_LIBRARY)
    #  define EXTENDBESTREFSHARED_EXPORT Q_DECL_EXPORT
    #else
    #  define EXTENDBESTREFSHARED_EXPORT Q_DECL_IMPORT
    #endif

    #endif // EXTENDBESTREF_GLOBAL_H

    ```
1. `extendbestref.h`
    ```h
    #ifndef EXTENDBESTREF_H
    #define EXTENDBESTREF_H

    #include "extendbestref_global.h"
    namespace TechiDaily {

    class EXTENDBESTREFSHARED_EXPORT ExtendBestRef
    {

    public:
        ExtendBestRef();
        const char* hi();
    };
    }

    #endif // EXTENDBESTREF_H
    ```
2. `extendbestref.cpp`

```cpp
#include "extendbestref.h"

namespace TechiDaily {

ExtendBestRef::ExtendBestRef()
{
}

const char* ExtendBestRef::hi()
{
    return "I'm ExtendBest Ref";
}
}
```

## 使用Qt Creator 创建Windows 动态库引用程序

```pro
#-------------------------------------------------
#
# Project created by QtCreator 2018-12-27T15:48:51
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = ExtendBestCall
TEMPLATE = app

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

CONFIG += c++11

SOURCES += \
        main.cpp \
        mainwindow.cpp

HEADERS += \
        mainwindow.h

FORMS += \
        mainwindow.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

```

## 添加引用库的方式

![](qmake/images/win-create-dynamic-library-06.jpg)
![](qmake/images/win-create-dynamic-library-07.jpg)
![](qmake/images/win-create-dynamic-library-08.jpg)

``` pro
# 添加第三方库
win32:CONFIG(release, debug|release): LIBS += -L$$PWD/../build-ExtendBestRef-Desktop_Qt_5_12_0_MinGW_64_bit-Debug/release/ -lExtendBestRef
else:win32:CONFIG(debug, debug|release): LIBS += -L$$PWD/../build-ExtendBestRef-Desktop_Qt_5_12_0_MinGW_64_bit-Debug/debug/ -lExtendBestRef

INCLUDEPATH += $$PWD/../ExtendBestRef
DEPENDPATH += $$PWD/../ExtendBestRef

INCLUDEPATH += $$PWD/../ExtendBestRef
DEPENDPATH += $$PWD/../ExtendBestRef
```

## 看一下，代码中如何调用

```cpp
#if defined __cplusplus
#include <iostream>
#endif

#include "mainwindow.h"
#include "ui_mainwindow.h"

#include "extendbestref.h" // 引用第三方库

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_testBtn_clicked()
{
    TechiDaily::ExtendBestRef ref;
#if defined __cplusplus
    std::cout << ref.hi() << std::endl;
#endif
}

```

##  运行的时候，需要将依赖库的dll文件，存放到可执行文件相同目录中

![](qmake/images/win-create-dynamic-library-09.jpg)
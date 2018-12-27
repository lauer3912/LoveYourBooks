# Linux 如何使用 Qt 创建静态库?

![](qmake/images/win-create-static-library-01.jpg)
![](qmake/images/win-create-static-library-02.jpg)
![](qmake/images/win-create-static-library-03.jpg)
![](qmake/images/win-create-static-library-04.jpg)
![](qmake/images/win-create-static-library-05.jpg)

## 使用Qt Creator 创建Windows 的静态库

查看 `\code-src\for_win\static_link_library\printor\PrintorRef\PrintorRef.pro` 文件内容

```pro
#-------------------------------------------------
#
# Project created by QtCreator 2018-12-27T14:06:49
#
#-------------------------------------------------

QT       -= gui

TARGET = PrintorRef
TEMPLATE = lib
CONFIG += staticlib #静态库

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
        printorref.cpp

HEADERS += \
        printorref.h
unix {
    target.path = /usr/lib
    INSTALLS += target
}
```

## 使用Qt Creator 创建Windows 桌面程序，引用静态库

查看 `code-src\for_win\static_link_library\printor\PrintorCall\PrintorCall.pro`

```pro
#-------------------------------------------------
#
# Project created by QtCreator 2018-12-27T14:16:32
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = PrintorCall
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

可以使用下面的方式，添加静态库引用

![](qmake/images/win-create-static-library-06.jpg)
![](qmake/images/win-create-static-library-07.jpg)
![](qmake/images/win-create-static-library-08.jpg)

最终，我们可以查看一下**整理后**的`PrintorCall.pro`文件内容

```pro
#-------------------------------------------------
#
# Project created by QtCreator 2018-12-27T14:16:32
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = PrintorCall
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

# 引用静态库
win32: LIBS += -L$$PWD/../build-PrintorRef-Desktop_Qt_5_12_0_MinGW_64_bit-Debug/debug/ -lPrintorRef

INCLUDEPATH += $$PWD/../PrintorRef
DEPENDPATH += $$PWD/../PrintorRef

win32:!win32-g++: PRE_TARGETDEPS += $$PWD/../build-PrintorRef-Desktop_Qt_5_12_0_MinGW_64_bit-Debug/debug/PrintorRef.lib
else:win32-g++: PRE_TARGETDEPS += $$PWD/../build-PrintorRef-Desktop_Qt_5_12_0_MinGW_64_bit-Debug/debug/libPrintorRef.a


# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

```

关键代码：

```pro
# 引用静态库
win32: LIBS += -L$$PWD/../build-PrintorRef-Desktop_Qt_5_12_0_MinGW_64_bit-Debug/debug/ -lPrintorRef

INCLUDEPATH += $$PWD/../PrintorRef
DEPENDPATH += $$PWD/../PrintorRef

win32:!win32-g++: PRE_TARGETDEPS += $$PWD/../build-PrintorRef-Desktop_Qt_5_12_0_MinGW_64_bit-Debug/debug/PrintorRef.lib
else:win32-g++: PRE_TARGETDEPS += $$PWD/../build-PrintorRef-Desktop_Qt_5_12_0_MinGW_64_bit-Debug/debug/libPrintorRef.a

```

## 下面，我们看一下静态库中的定义内容

`printorref.h` 文件

```h
#ifndef PRINTORREF_H
#define PRINTORREF_H

namespace TechiDaily {
class PrintorRef
{

public:
    PrintorRef();
    const char* hi();
};
}

#endif // PRINTORREF_H
```

`printorref.cpp` 文件

```c++
#include "printorref.h"


namespace TechiDaily {
//![0]
PrintorRef::PrintorRef()
{
}

const char *PrintorRef::hi()
{
    return "Hi! I'm PrintorRef";
}
//![0]
}

```

## 下面我们看一下调用者的代码

```cpp
#if defined __cplusplus
#include <iostream>
#endif

#include "mainwindow.h"
#include "ui_mainwindow.h"

#include "printorref.h" // 引用第三方库

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
    TechiDaily::PrintorRef ref;
#if defined __cplusplus
    std::cout << ref.hi() << std::endl;
#endif

}

```
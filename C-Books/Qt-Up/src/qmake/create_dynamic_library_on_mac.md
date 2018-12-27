# MacOS 如何使用 Qt 创建动态库?

## 使用 Qt Creator 创建动态 library, 我们得到最初的`pro`文件

![](qmake/images/mac-create-dynamic-library-01.png)
![](qmake/images/mac-create-dynamic-library-02.png)
![](qmake/images/mac-create-dynamic-library-03.png)
![](qmake/images/mac-create-dynamic-library-04.png)
![](qmake/images/mac-create-dynamic-library-05.png)

`/code-src/for_mac/dynamic_link_library/linear/linearRef/linearRef.pro` 文件内容

```pro
#-------------------------------------------------
#
# Project created by QtCreator 2018-12-27T08:58:42
#
#-------------------------------------------------

QT       -= gui

TARGET = linearRef
TEMPLATE = lib

DEFINES += LINEARREF_LIBRARY

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
        linearref.cpp

HEADERS += \
        linearref.h \
        linearref_global.h

unix {
    target.path = /usr/lib
    INSTALLS += target
}

```

## 使用 Qt Creator 创建一个桌面应用, 我们得到最初的`pro`文件

查看 `/code-src/for_mac/dynamic_link_library/linear/linearApp/linearApp.pro` 文件内容

```toml
#-------------------------------------------------
#
# Project created by QtCreator 2018-12-27T09:06:42
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = linearApp
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

## 加入引用动态库的代码

现在在观察一下`/code-src/for_mac/dynamic_link_library/linear/linearApp/linearApp.pro` 文件内容

```Pro
#-------------------------------------------------
#
# Project created by QtCreator 2018-12-27T09:06:42
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = linearApp
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

# 链接外部库
macx {
    LIBS += -L$$PWD/../build-linearRef-Desktop_Qt_5_12_0_clang_64bit2-Debug/ -llinearRef.1.0.0
    INCLUDEPATH += $$PWD/../linearRef
    DEPENDPATH += $$PWD/../linearRef
}

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target



```

## 现在查看代码的变化

`code-src/for_mac/dynamic_link_library/linear/linearRef/linearref_global.h`

```h
#ifndef LINEARREF_GLOBAL_H
#define LINEARREF_GLOBAL_H

#include <QtCore/qglobal.h>

#if defined(LINEARREF_LIBRARY)
#  define LINEARREFSHARED_EXPORT Q_DECL_EXPORT
#else
#  define LINEARREFSHARED_EXPORT Q_DECL_IMPORT
#endif

#endif // LINEARREF_GLOBAL_H
```

**注意：新建了 LINEARREFSHARED_EXPORT 宏**

`code-src/for_mac/dynamic_link_library/linear/linearRef/linearref.h`

```h
#ifndef LINEARREF_H
#define LINEARREF_H

#include "linearref_global.h"

namespace TechiDaily{
class LINEARREFSHARED_EXPORT LinearRef
{

public:
    LinearRef();
    const char* getName();
};
}


#endif // LINEARREF_H

```

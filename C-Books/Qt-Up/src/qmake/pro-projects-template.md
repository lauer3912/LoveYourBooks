# Pro 工程模板

模板文件，用于更明确的说明，编码用途

| Template  | qmake Output                                                      |
| --------- | ----------------------------------------------------------------- |
| app       | Makefile to build an application.                                 |
| lib       | Makefile to build a library.                                      |
| vcapp     | Visual Studio Project file to build an application.               |
| vclib     | Visual Studio Project file to build a library.                    |
| vcsubdirs | Visual Studio Solution file to build projects in sub-directories. |

具体详细部分：参照 [doc.qt.io/qt-5/qmake-project-files.html](http://doc.qt.io/qt-5/qmake-project-files.html)

关于以 QT 为前缀的变量有

具体详细部分：参照 [http://doc.qt.io/qt-5/qmake-variable-reference.html#qt](http://doc.qt.io/qt-5/qmake-variable-reference.html#qt)

介绍 qmake
qmake 是用来为不同的平台的开发项目创建 makefile 的 Trolltech 开发一个易于使用的工具。qmake 简化了 makefile 的生成，所以为了创建一个 makefile 只需要一个只有几行信息的文件。qmake 可以供任何一个软件项目使用，而不用管它是不是用 Qt 写的，尽管它包含了为支持 Qt 开发所拥有的额外的特征。

qmake 基于一个项目文件这样的信息来生成 makefile。项目文件可以由开发者生成。项目文件通常很简单，但是如果需要它是非常完善的。不用修改项目文件，qmake 也可以为为 Microsoft Visual Studio 生成项目。

qmake 的概念
QMAKESPEC 环境变量
举例来说，如果你在 Windows 下使用 Microsoft Visual Studio，然后你需要把 QMAKESPEC 环境变量设置为 win32-msvc。如果你在 Solaris 上使用 gcc，你需要把 QMAKESPEC 环境变量设置为 solaris-g++。

在 qt/mkspecs 中的每一个目录里面，都有一个包含了平台和编译器特定信息的 qmake.conf 文件。这些设置适用于你要使用 qmake 的任何项目，请不要修改它，除非你是一个专家。例如，假如你所有的应用程序都必须和一个特定的库连接，你可以把这个信息添加到相应的 qmake.conf 文件中。

项目(.pro)文件
一个项目文件是用来告诉 qmake 关于为这个应用程序创建 makefile 所需要的细节。例如，一个源文件和头文件的列表、任何应用程序特定配置、例如一个必需要连接的额外库、或者一个额外的包含路径，都应该放到项目文件中。

“#”注释
你可以为项目文件添加注释。注释由“#”符号开始，一直到这一行的结束。

模板
模板变量告诉 qmake 为这个应用程序生成哪种 makefile。下面是可供使用的选择：

app - 建立一个应用程序的 makefile。这是默认值，所以如果模板没有被指定，这个将被使用。

lib - 建立一个库的 makefile。

vcapp - 建立一个应用程序的 Visual Studio 项目文件。

vclib - 建立一个库的 Visual Studio 项目文件。

subdirs - 这是一个特殊的模板，它可以创建一个能够进入特定目录并且为一个项目文件生成 makefile 并且为它调用 make 的 makefile。

“app”模板
“app”模板告诉 qmake 为建立一个应用程序生成一个 makefile。当使用这个模板时，下面这些 qmake 系统变量是被承认的。你应该在你的.pro 文件中使用它们来为你的应用程序指定特定信息。

HEADERS - 应用程序中的所有头文件的列表。

SOURCES - 应用程序中的所有源文件的列表。

FORMS - 应用程序中的所有.ui 文件（由 Qt 设计器生成）的列表。

LEXSOURCES - 应用程序中的所有 lex 源文件的列表。

YACCSOURCES - 应用程序中的所有 yacc 源文件的列表。

TARGET - 可执行应用程序的名称。默认值为项目文件的名称。（如果需要扩展名，会被自动加上。）

DESTDIR - 放置可执行程序目标的目录。

DEFINES - 应用程序所需的额外的预处理程序定义的列表。

INCLUDEPATH - 应用程序所需的额外的包含路径的列表。

DEPENDPATH - 应用程序所依赖的搜索路径。

VPATH - 寻找补充文件的搜索路径。

DEF_FILE - 只有 Windows 需要：应用程序所要连接的.def 文件。

RC_FILE - 只有 Windows 需要：应用程序的资源文件。

RES_FILE - 只有 Windows 需要：应用程序所要连接的资源文件。

你只需要使用那些你已经有值的系统变量，例如，如果你不需要任何额外的 INCLUDEPATH，那么你就不需要指定它，qmake 会为所需的提供默认值。例如，一个实例项目文件也许就像这样：

TEMPLATE = app
DESTDIR = c:\helloapp
HEADERS += hello.h
SOURCES += hello.cpp
SOURCES += main.cpp
DEFINES += QT_DLL
CONFIG += qt warn_on release
如果条目是单值的，比如 template 或者目的目录，我们是用“=”，但如果是多值条目，我们使用“+=”来为这个类型添加现有的条目。使用“=”会用新值替换原有的值，例如，如果我们写了 DEFINES=QT_DLL，其它所有的定义都将被删除。

“lib”模板
“lib”模板告诉 qmake 为建立一个库而生成 makefile。当使用这个模板时，除了“app”模板中提到系统变量，还有一个 VERSION 是被支持的。你需要在为库指定特定信息的.pro 文件中使用它们。

VERSION - 目标库的版本号，比如，2.3.1。

“subdirs”模板
“subdirs”模板告诉 qmake 生成一个 makefile，它可以进入到特定子目录并为这个目录中的项目文件生成 makefile 并且为它调用 make。

在这个模板中只有一个系统变量 SUBDIRS 可以被识别。这个变量中包含了所要处理的含有项目文件的子目录的列表。这个项目文件的名称是和子目录同名的，这样 qmake 就可以发现它。例如，如果子目里是“myapp”，那么在这个目录中的项目文件应该被叫做 myapp.pro。

CONFIG 变量
配置变量指定了编译器所要使用的选项和所需要被连接的库。配置变量中可以添加任何东西，但只有下面这些选项可以被 qmake 识别。

下面这些选项控制着使用哪些编译器标志：

release - 应用程序将以 release 模式连编。如果“debug”被指定，它将被忽略。

debug - 应用程序将以 debug 模式连编。

warn_on - 编译器会输出尽可能多的警告信息。如果“warn_off”被指定，它将被忽略。

warn_off - 编译器会输出尽可能少的警告信息。

下面这些选项定义了所要连编的库/应用程序的类型：

qt - 应用程序是一个 Qt 应用程序，并且 Qt 库将会被连接。

thread - 应用程序是一个多线程应用程序。

x11 - 应用程序是一个 X11 应用程序或库。

windows - 只用于“app”模板：应用程序是一个 Windows 下的窗口应用程序。

console - 只用于“app”模板：应用程序是一个 Windows 下的控制台应用程序。

dll - 只用于“lib”模板：库是一个共享库（dll）。

staticlib - 只用于“lib”模板：库是一个静态库。

plugin - 只用于“lib”模板：库是一个插件，这将会使 dll 选项生效。

例如，如果你的应用程序使用 Qt 库，并且你想把它连编为一个可调试的多线程的应用程序，你的项目文件应该会有下面这行：

    CONFIG += qt thread debug

注意，你必须使用“+=”，不要使用“=”，否则 qmake 就不能正确使用连编 Qt 的设置了，比如没法获得所编译的 Qt 库的类型了。

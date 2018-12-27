# Qmake 高级概念

[英文部分 http://doc.qt.io/qt-5/qmake-language.html](http://doc.qt.io/qt-5/qmake-language.html)
qmake 高级概念
迄今为止，我们见到的 qmake 项目文件都非常简单，仅仅是一些 name = value 和 name += value 的列表行。qmake 提供了很多更强大的功能，比如你可以使用一个简单的项目文件来为多个平台生成 makefile。

操作符
到目前为止，你已经看到在项目文件中使用的=操作符和+=操作符。这里能够提供更多的可供使用的操作符，但是其中的一些需要谨慎地使用，因为它们也许会比你期待的改变的更多。

“=”操作符
这个操作符简单分配一个值给一个变量。使用方法如下：

    TARGET = myapp

这将会设置 TARGET 变量为 myapp。这将会删除原来对 TARGET 的任何设置。

“+=”操作符
这个操作符将会向一个变量的值的列表中添加一个值。使用方法如下：

    DEFINES += QT_DLL

这将会把 QT_DLL 添加到被放到 makefile 中的预处理定义的列表中。

“-=”操作符
这个操作符将会从一个变量的值的列表中移去一个值。使用方法如下：

    DEFINES -= QT_DLL

这将会从被放到 makefile 中的预处理定义的列表中移去 QT_DLL。

“\*=”操作符
这个操作符仅仅在一个值不存在于一个变量的值的列表中的时候，把它添加进去。使用方法如下：

    DEFINES *= QT_DLL

只用在 QT_DLL 没有被定义在预处理定义的列表中时，它才会被添加进去。

“~=”操作符
这个操作符将会替换任何与指定的值的正则表达式匹配的任何值。使用方法如下：

    DEFINES ~= s/QT_[DT].+/QT

这将会用 QT 来替代任何以 QT_D 或 QT_T 开头的变量中的 QT_D 或 QT_T。

作用域
作用域和“if”语句很相似，如果某个条件为真，作用域中的设置就会被处理。作用域使用方法如下：

    win32 {
        DEFINES += QT_DLL
    }

上面的代码的作用是，如果在 Windows 平台上使用 qmake，QT_DLL 定义就会被添加到 makefile 中。如果在 Windows 平台以外的平台上使用 qmake，这个定义就会被忽略。你也可以使用 qmake 执行一个单行的条件/任务，就像这样：

    win32:DEFINES += QT_DLL

比如，假设我们想在除了 Windows 平台意外的所有平台处理些什么。我们想这样使用作用域来达到这种否定效果：

    !win32 {
        DEFINES += QT_DLL
    }

CONFIG 行中的任何条目也都是一个作用域。比如，你这样写：

    CONFIG += warn_on

你将会得到一个称作“warn_on”的作用域。这样将会使在不丢失特定条件下可能所需的所有自定义设置的条件下，很容易地修改项目中的配置。因为你可能把你自己的值放到 CONFIG 行中，这将会为你的 makefile 而提供给你一个非常强大的配置工具。比如：

    CONFIG += qt warn_on debug
    debug {
        TARGET = myappdebug
    }
    release {
        TARGET = myapp
    }

在上面的代码中，两个作用域被创建，它们依赖于 CONFIG 行中设置的是什么。在这个例子中，debug 在 CONFIG 行中，所以 TARGET 变量被设置为 myappdebug。如果 release 在 CONFIG 行中，那么 TARGET 变量将会被设置为 myapp。

当然也可以在处理一些设置之前检查两个事物。例如，如果你想检查平台是否是 Windows 并且线程设置是否被设定，你可以这样写：

    win32 {
        thread {
            DEFINES += QT_THREAD_SUPPORT
        }
    }

为了避免写出许多嵌套作用域，你可以这样使用冒号来嵌套作用域：

    win32:thread {
        DEFINES += QT_THREAD_SUPPORT
    }

一旦一个测试被执行，你也许也要做 else/elseif 操作。这种情况下，你可以很容易地写出复杂的测试。这需要使用特殊的“else”作用域，它可以和其它作用域进行组合（也可以向上面一样使用冒号），比如：

    win32:thread {
        DEFINES += QT_THREAD_SUPPORT
    } else:debug {
        DEFINES += QT_NOTHREAD_DEBUG
    } else {
        warning("Unknown configuration")
    }

变量
到目前为止我们遇到的变量都是系统变量，比如 DEFINES、SOURCES 和 HEADERS。你也可以为你自己创建自己的变量，这样你就可以在作用域中使用它们了。创建自己的变量很容易，只要命名它并且分配一些东西给它。比如：

    MY_VARIABLE = value

现在你对你自己的变量做什么是没有限制的，同样地，qmake 将会忽略它们，除非需要在一个作用域中考虑它们。

你也可以通过在其它任何一个变量的变量名前加\$\$来把这个变量的值分配给当前的变量。例如：

    MY_DEFINES = $$DEFINES

现在 MY_DEFINES 变量包含了项目文件在这点时 DEFINES 变量的值。这也和下面的语句一样：

    MY_DEFINES = $${DEFINES}

第二种方法允许你把一个变量和其它变量连接起来，而不用使用空格。qmake 将允许一个变量包含任何东西（包括$(VALUE)，可以直接在makefile中直接放置，并且允许它适当地扩张，通常是一个环境变量）。无论如何，如果你需要立即设置一个环境变量，然后你就可以使用$\$()方法。比如：

    MY_DEFINES = $$(ENV_DEFINES)

这将会设置 MY_DEFINES 为环境变量 ENV_DEFINES 传递给.pro 文件地值。另外你可以在替换的变量里调用内置函数。这些函数（不会和下一节中列举的测试函数混淆）列出如下：

join( variablename, glue, before, after )
这将会在 variablename 的各个值中间加入 glue。如果这个变量的值为非空，那么就会在值的前面加一个前缀 before 和一个后缀 after。只有 variablename 是必须的字段，其它默认情况下为空串。如果你需要在 glue、before 或者 after 中使用空格的话，你必须提供它们。

member( variablename, position )
这将会放置 variablename 的列表中的 position 位置的值。如果 variablename 不够长，这将会返回一个空串。variablename 是唯一必须的字段，如果没有指定位置，则默认为列表中的第一个值。

find( variablename, substr )
这将会放置 variablename 中所有匹配 substr 的值。substr 也可以是正则表达式，而因此将被匹配。

    MY_VAR = one two three four
    MY_VAR2 = $$join(MY_VAR, " -L", -L) -Lfive
    MY_VAR3 = $$member(MY_VAR, 2) $$find(MY_VAR, t.*)

MY_VAR2 将会包含“-Lone -Ltwo -Lthree -Lfour -Lfive”，并且 MYVAR3 将会包含“three two three”。

system( program_and_args )
这将会返回程序执行在标准输出/标准错误输出的内容，并且正像平时所期待地分析它。比如你可以使用这个来询问有关平台的信息。

    UNAME = $$system(uname -s)
    contains( UNAME, [lL]inux ):message( This looks like Linux ($$UNAME) to me )

测试函数
qmake 提供了可以简单执行，但强大测试的内置函数。这些测试也可以用在作用域中（就像上面一样），在一些情况下，忽略它的测试值，它自己使用测试函数是很有用的。

contains( variablename, value )
如果 value 存在于一个被叫做 variablename 的变量的值的列表中，那么这个作用域中的设置将会被处理。例如：

    contains( CONFIG, thread ) {
        DEFINES += QT_THREAD_SUPPORT
    }

如果 thread 存在于 CONFIG 变量的值的列表中时，那么 QT_THREAD_SUPPORT 将会被加入到 DEFINES 变量的值的列表中。

count( variablename, number )
如果 number 与一个被叫做 variablename 的变量的值的数量一致，那么这个作用域中的设置将会被处理。例如：

    count( DEFINES, 5 ) {
        CONFIG += debug
    }

error( string )
这个函数输出所给定的字符串，然后会使 qmake 退出。例如：

    error( "An error has occured" )

文本“An error has occured”将会被显示在控制台上并且 qmake 将会退出。

exists( filename )
如果指定文件存在，那么这个作用域中的设置将会被处理。例如：

    exists( /local/qt/qmake/main.cpp ) {
        SOURCES += main.cpp
    }

如果/local/qt/qmake/main.cpp 存在，那么 main.cpp 将会被添加到源文件列表中。

注意可以不用考虑平台使用“/”作为目录的分隔符。

include( filename )
项目文件在这一点时包含这个文件名的内容，所以指定文件中的任何设置都将会被处理。例如：

    include( myotherapp.pro )

myotherapp.pro 项目文件中的任何设置现在都会被处理。

isEmpty( variablename )
这和使用 count( variablename, 0 )是一样的。如果叫做 variablename 的变量没有任何元素，那么这个作用域中的设置将会被处理。例如：

    isEmpty( CONFIG ) {
        CONFIG += qt warn_on debug
    }

message( string )
这个函数只是简单地在控制台上输出消息。

    message( "This is a message" )

文本“This is a message”被输出到控制台上并且对于项目文件的处理将会继续进行。

system( command )
特定指令被执行并且如果它返回一个 1 的退出值，那么这个作用域中的设置将会被处理。例如：

    system( ls /bin ) {
        SOURCES += bin/main.cpp
        HEADERS += bin/main.h
    }

所以如果命令 ls /bin 返回 1，那么 bin/main.cpp 将被添加到源文件列表中并且 bin/main.h 将被添加到头文件列表中。

infile( filename, var, val )
如果 filename 文件（当它被 qmake 自己解析时）包含一个值为 val 的变量 var，那么这个函数将会返回成功。你也可以不传递第三个参数（val），这时函数将只测试文件中是否分配有这样一个变量 var。

# 快速入门

[http://doc.qt.io/qt-5/qmake-tutorial.html](http://doc.qt.io/qt-5/qmake-tutorial.html)

Getting Started

This tutorial teaches you the basics of qmake. The other topics in this manual contain more detailed information about using qmake.
Starting Off Simple

Let's assume that you have just finished a basic implementation of your application, and you have created the following files:

```text
    hello.cpp
    hello.h
    main.cpp
```

You will find these files in the examples/qmake/tutorial directory of the Qt distribution. The only other thing you know about the setup of the application is that it's written in Qt. First, using your favorite plain text editor, create a file called hello.pro in examples/qmake/tutorial. The first thing you need to do is add the lines that tell qmake about the source and header files that are part of your development project.

We'll add the source files to the project file first. To do this you need to use the SOURCES variable. Just start a new line with SOURCES += and put hello.cpp after it. You should have something like this:

```pro
SOURCES += hello.cpp
```

We repeat this for each source file in the project, until we end up with the following:

```pro
SOURCES += hello.cpp
SOURCES += main.cpp
```

If you prefer to use a Make-like syntax, with all the files listed in one go you can use the newline escaping like this:

```pro
SOURCES = hello.cpp \
          main.cpp
```

Now that the source files are listed in the project file, the header files must be added. These are added in exactly the same way as source files, except that the variable name we use is HEADERS.

Once you have done this, your project file should look something like this:

```pro
HEADERS += hello.h
SOURCES += hello.cpp
SOURCES += main.cpp
```

The target name is set automatically. It is the same as the project filename, but with the suffix appropriate for the platform. For example, if the project file is called hello.pro, the target will be hello.exe on Windows and hello on Unix. If you want to use a different name you can set it in the project file:

```pro
TARGET = helloworld
```

The finished project file should look like this:

```pro
HEADERS += hello.h
SOURCES += hello.cpp
SOURCES += main.cpp
```

You can now use qmake to generate a Makefile for your application. On the command line, in your project directory, type the following:

```bash
qmake -o Makefile hello.pro
```

Then type make or nmake depending on the compiler you use.

For Visual Studio users, qmake can also generate Visual Studio project files. For example:

```bash
qmake -tp vc hello.pro
```

Making an Application Debuggable

The release version of an application does not contain any debugging symbols or other debugging information. During development, it is useful to produce a debugging version of the application that has the relevant information. This is easily achieved by adding debug to the CONFIG variable in the project file.

For example:

```pro
CONFIG += debug
HEADERS += hello.h
SOURCES += hello.cpp
SOURCES += main.cpp
```

Use qmake as before to generate a Makefile. You will now obtain useful information about your application when running it in a debugging environment.
Adding Platform-Specific Source Files

After a few hours of coding, you might have made a start on the platform-specific part of your application, and decided to keep the platform-dependent code separate. So you now have two new files to include into your project file: hellowin.cpp and hellounix.cpp. We cannot just add these to the SOURCES variable since that would place both files in the Makefile. So, what we need to do here is to use a scope which will be processed depending on which platform we are building for.

A simple scope that adds the platform-dependent file for Windows looks like this:

```pro
win32 {
    SOURCES += hellowin.cpp
}
```

When building for Windows, qmake adds hellowin.cpp to the list of source files. When building for any other platform, qmake simply ignores it. Now all that is left to be done is to create a scope for the Unix-specific file.

When you have done that, your project file should look something like this:

```pro
CONFIG += debug
HEADERS += hello.h
SOURCES += hello.cpp
SOURCES += main.cpp
win32 {
    SOURCES += hellowin.cpp
}
unix {
    SOURCES += hellounix.cpp
}
```

Use qmake as before to generate a Makefile.
Stopping qmake If a File Does Not Exist

You may not want to create a Makefile if a certain file does not exist. We can check if a file exists by using the exists() function. We can stop qmake from processing by using the error() function. This works in the same way as scopes do. Simply replace the scope condition with the function. A check for a file called main.cpp looks like this:

```pro
!exists( main.cpp ) {
    error( "No main.cpp file found" )
}
```

The ! symbol is used to negate the test. That is, exists( main.cpp ) is true if the file exists, and !exists( main.cpp ) is true if the file does not exist.

````pro
CONFIG += debug
HEADERS += hello.h
SOURCES += hello.cpp
SOURCES += main.cpp
win32 {
    SOURCES += hellowin.cpp
}
unix {
    SOURCES += hellounix.cpp
}
!exists( main.cpp ) {
    error( "No main.cpp file found" )
}
```pro

Use qmake as before to generate a makefile. If you rename main.cpp temporarily, you will see the message and qmake will stop processing.
Checking for More than One Condition

Suppose you use Windows and you want to be able to see statement output with qDebug() when you run your application on the command line. To see the output, you must build your application with the appropriate console setting. We can easily put console on the CONFIG line to include this setting in the Makefile on Windows. However, let's say that we only want to add the CONFIG line when we are running on Windows and when debug is already on the CONFIG line. This requires using two nested scopes. First create one scope, then create the other inside it. Put the settings to be processed inside the second scope, like this:

```pro
win32 {
    debug {
        CONFIG += console
    }
}
````

Nested scopes can be joined together using colons, so the final project file looks like this:

```pro
CONFIG += debug
HEADERS += hello.h
SOURCES += hello.cpp
SOURCES += main.cpp
win32 {
    SOURCES += hellowin.cpp
}
unix {
    SOURCES += hellounix.cpp
}
!exists( main.cpp ) {
    error( "No main.cpp file found" )
}
win32:debug {
    CONFIG += console
}
```

That's it! You have now completed the tutorial for qmake, and are ready to write project files for your development projects.

qmake 教程介绍
这个教程可以教会你如何使用 qmake。我们建议你看完这个教程之后读一下 qmake 手册。

开始很简单
让我们假设你已经完成了你的应用程序的一个基本实现，并且你已经创建了下述文件：

hello.cpp

hello.h

main.cpp

你可以在 qt/qmake/example 中发现这些文件。你对这个应用程序的配置仅仅知道的另一件事是它是用 Qt 写的。首先，使用你所喜欢的纯文本编辑器，在 qt/qmake/tutorial 中创建一个叫做 hello.pro 的文件。你所要做的第一件事是添加一些行来告诉 qmake 关于你所开发的项目中的源文件和头文件这一部分。

我们先把源文件添加到项目文件中。为了做到这点，你需要使用 SOURCES 变量。只要用 SOURCES +=来开始一行，并且把 hello.cpp 放到它后面。你需要写成这样：

    SOURCES += hello.cpp

我们对项目中的每一个源文件都这样做，直到结束：

    SOURCES += hello.cpp
    SOURCES += main.cpp

如果你喜欢使用像 Make 一样风格的语法，你也可以写成这样，一行写一个源文件，并用反斜线结尾，然后再起新的一行：

    SOURCES = hello.cpp \
          main.cpp

现在源文件已经被列到项目文件中了，头文件也必须添加。添加的方式和源文件一样，除了变量名是 HEADERS。

当你做完这些时，你的项目文件就像现在这样：

    HEADERS += hello.h
    SOURCES += hello.cpp
    SOURCES += main.cpp

目标名称是自动设置的，它被设置为和项目文件一样的名称，但是为了适合平台所需要的后缀。举例来说，加入项目文件叫做“hello.pro”，在 Windows 上的目标名称应该是“hello.exe”，在 Unix 上应该是“hello”。如果你想设置一个不同的名字，你可以在项目文件中设置它：

    TARGET = helloworld

最后一步是设置 CONFIG 变量。因为这是一个 Qt 应用程序，我们需要把“qt”放到 CONFIG 这一行中，这样 qmake 才会在连接的时候添加相关的库，并且保证 moc 和 uic 的连编行也被包含到 Makefile 中。

最终完成的项目文件应该是这样的：

    CONFIG += qt
    HEADERS += hello.h
    SOURCES += hello.cpp
    SOURCES += main.cpp

你现在可以使用 qmake 来为你的应用程序生成 Makefile。在你的应用程序目录中，在命令行下输入：

    qmake -o Makefile hello.pro

然后根据你所使用的编译器输入 make 或者 nmake。

使应用程序可以调试
应用程序的发布版本不包含任何调试符号或者其它调试信息。在开发过程中，生成一个含有相关信息的应用程序的调试版本是很有用处的。通过在项目文件的 CONFIG 变量中添加“debug”就可以很简单地实现。

例如：

    CONFIG += qt debug
    HEADERS += hello.h
    SOURCES += hello.cpp
    SOURCES += main.cpp

像前面一样使用 qmake 来生成一个 Makefile 并且你就能够调试你的应用程序了。

添加特定平台的源文件
在编了几个小时的程序之后，你也许开始为你的应用程序编写与平台相关的部分，并且决定根据平台的不同编写不同的代码。所以现在你有两个信文件要包含到你的项目文件中－hello_win.cpp 和 hello_x11.cpp。我们不能仅仅把这两个文件放到 SOURCES 变量中，因为那样的话会把这两个文件都加到 Makefile 中。所以我们在这里需要做的是根据 qmake 所运行的平台来使用相应的作用域来进行处理。

为 Windows 平台添加的依赖平台的文件的简单的作用域看起来就像这样：

    win32 {
    SOURCES += hello_win.cpp
    }

所以如果 qmake 运行在 Windows 上的时候，它就会把 hello_win.cpp 添加到源文件列表中。如果 qmake 运行在其它平台上的时候，它会很简单地把这部分忽略。现在接下来我们要做的就是添加一个 X11 依赖文件的作用域。

当你做完了这部分，你的项目文件应该和这样差不多：

    CONFIG += qt debug
    HEADERS += hello.h
    SOURCES += hello.cpp
    SOURCES += main.cpp
    win32 {
    SOURCES += hello_win.cpp
    }
    x11 {
    SOURCES += hello_x11.cpp
    }

像前面一样使用 qmake 来生成 Makefile。

如果一个文件不存在，停止 qmake
如果某一个文件不存在的时候，你也许不想生成一个 Makefile。我们可以通过使用 exists()函数来检查一个文件是否存在。我们可以通过使用 error()函数把正在运行的 qmake 停下来。这和作用域的工作方式一样。只要很简单地用这个函数来替换作用域条件。对 main.cpp 文件的检查就像这样：

    !exists( main.cpp ) {
    error( "No main.cpp file found" )
    }

“!”用来否定这个测试，比如，如果文件存在，exists( main.cpp )是真，如果文件不存在，!exists( main.cpp )是真。

    CONFIG += qt debug
    HEADERS += hello.h
    SOURCES += hello.cpp
    SOURCES += main.cpp
    win32 {
    SOURCES += hello_win.cpp
    }
    x11 {
    SOURCES += hello_x11.cpp
    }
    !exists( main.cpp ) {
    error( "No main.cpp file found" )
    }

像前面一样使用 qmake 来生成 Makefile。如果你临时改变 main.cpp 的名称，你会看到信息，并且 qmake 会停止处理。

检查多于一个的条件
假设你使用 Windows 并且当你在命令行运行你的应用程序的时候你想能够看到 qDebug()语句。除非你在连编你的程序的时候使用 console 设置，你不会看到输出。我们可以很容易地把 console 添加到 CONFIG 行中，这样在 Windows 下，Makefile 就会有这个设置。但是如果告诉你我们只是想在当我们的应用程序运行在 Windows 下并且当 debug 已经在 CONFIG 行中的时候，添加 console。这需要两个嵌套的作用域；只要生成一个作用域，然后在它里面再生成另一个。把设置放在最里面的作用域里，就像这样：

    win32 {
    debug {
        CONFIG += console
    }
    }

嵌套的作用域可以使用冒号连接起来，所以最终的项目文件看起来像这样：

    CONFIG += qt debug
    HEADERS += hello.h
    SOURCES += hello.cpp
    SOURCES += main.cpp
    win32 {
    SOURCES += hello_win.cpp
    }
    x11 {
    SOURCES += hello_x11.cpp
    }
    !exists( main.cpp ) {
    error( "No main.cpp file found" )
    }
    win32:debug {
    CONFIG += console
    }

就这些了！你现在已经完成了 qmake 的教程，并且已经准备好为你的开发项目写项目文件了。

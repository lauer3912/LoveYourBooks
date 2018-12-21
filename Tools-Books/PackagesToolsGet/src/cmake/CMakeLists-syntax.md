# CMakeLists.txt 语法

## project

    语句 : project(<projectname> [languageName1 languageName2 … ] )
    作用 : 指定项目名

## cmake_minimum_required

    语句 : cmake_minimum_required(VERSION major[.minor[.patch[.tweak]]] [FATAL_ERROR])
    作用 : 指定cmake需要的最小版本

## aux_source_directory

    语句 : aux_source_directory(<dir> <variable>)
    作用 : 获取指定目录下的所有文件,保存到variable中,包括 .c .C .c++ .cc .cpp .cxx .m .M .mm .h .hh .h++ .hm .hpp .hxx .in .txx文件
    示例 : aux_source_directory(. var)#获取当前目录中源文件

## add_executable

    语句 : add_executable(<name> [WIN32] [MACOSX_BUNDLE] [EXCLUDE_FROM_ALL] source1 source2 … sourceN)
    作用 : 将指定文件source编译成可执行文件,命名位name
    示例 : add_executable(hello hello.cpp)

## add_library

    语句 : add_library([STATIC | SHARED | MODULE] [EXCLUDE_FROM_ALL] source1 source2 … sourceN)
    作用 : 添加一个名为<name>的库文件，指定STATIC，SHARED，或者MODULE参数用来指定要创建的库的类型。STATIC库是目标文件的归档文件，在链接其它目标的时候使用。SHARED库会被动态链接，在运行时被加载。MODULE库是不会被链接到其它目标中的插件，但是可能会在运行时使用dlopen-系列的函数动态链接。如果没有类型被显式指定，这个选项将会根据变量BUILD_SHARED_LIBS的当前值是否为真决定是STATIC还是SHARED
    示例 : add_library(Lib ${DIR_SRCS})

## add_dependencies

    语句 : add_dependencies(target-name depend-target1 depend-target2 …)
    作用 : 用于指定某个目标（可执行文件或者库文件）依赖于其他的目标。这里的目标必须是 add_executable、add_library、add_custom_target 命令创建的目标

## add_subdirectory

    语句 : add_subdirectory(source_dir [binary_dir] [EXCLUDE_FROM_ALL])
    作用 : 用于添加一个需要进行构建的子目录
    示例 : add_subdirectory(directory)

## target_link_libraries

    语句 : target_link_libraries(<target> [item1 [item2 […]]] [[debug|optimized|general] ] …)
    作用 : 用于指定 target 需要链接 item1 item2 …。这里 target 必须已经被创建，链接的 item 可以是已经存在的 target（依赖关系会自动添加）
    示例 : target_link_libraries(Main Lib)

## set

    语句 : set(<variable> <value> [[CACHE <type> <docstring> [FORCE]] | PARENT_SCOPE])
    作用 : 用于设定变量 variable 的值为 value。variable可以自己定义
    示例 : set(var "${list}_exe")

## unset

    语句 : unset(<variable> [CACHE])

    作用 : 用于移除变量 variable。如果指定了 CACHE 变量将被从 Cache 中移除。

    示例 : unset(VAR CACHE)

## message

    语句 : message([STATUS|WARNING|AUTHOR_WARNING|FATAL_ERROR|SEND_ERROR] “message to display” …)
    作用 : 输出信息
    示例 : message("hello world")

## include_directories

    语句 : include_directories([AFTER|BEFORE] [SYSTEM] dir1 dir2 …)
    作用 : 用于设定目录，这些设定的目录将被编译器用来查找 include 文件
    示例 : include_directories(${PROJECT_SOURCE_DIR}/lib)

## find_path

    语句 : find_path(<VAR> name1 [path1 path2 …])
    作用 : 用于查找包含文件 name1 的路径，如果找到则将路径保存在 VAR 中（此路径为一个绝对路径），如果没有找到则结果为 <VAR>-NOTFOUND。默认的情况下，VAR 会被保存在 Cache 中，这时候我们需要清除 VAR 才可以进行下一次查询（使用 unset 命令）

## add_definitions

    语句 : find_library(<VAR> name1 [path1 path2 …])
    作用 : 用于添加编译器命令行标志（选项），通常的情况下我们使用其来添加预处理器定义
    示例 : add_definitions(-D_UNICODE -DUNICODE)

## execute_process

    语句 : execute_process(COMMAND <cmd1> [args1...]]  [COMMAND <cmd2> [args2...] [...]]
                                            [WORKING_DIRECTORY <directory>]
                                            [TIMEOUT <seconds>]
                                            [RESULT_VARIABLE <variable>]
                                            [OUTPUT_VARIABLE <variable>]
                                            [ERROR_VARIABLE <variable>]
                                            [INPUT_FILE <file>]
                                            [OUTPUT_FILE <file>]
                                            [ERROR_FILE <file>]
                                            [OUTPUT_QUIET]
                                            [ERROR_QUIET]
                                            [OUTPUT_STRIP_TRAILING_WHITESPACE]
                                            [ERROR_STRIP_TRAILING_WHITESPACE])
    作用 : 用于执行一个或者多个外部命令。每一个命令的标准输出通过管道转为下一个命令的标准输入。WORKING_DIRECTORY 用于指定外部命令的工作目录，RESULT_VARIABLE 用于指定一个变量保存外部命令执行的结果，这个结果可能是最后一个执行的外部命令的退出码或者是一个描述错误条件的字符串，OUTPUT_VARIABLE 或者 ERROR_VARIABLE 用于指定一个变量保存标准输出或者标准错误，OUTPUT_QUIET 或者 ERROR_QUIET 用于忽略标准输出和标准错误。
    示例 : execute_process(COMMAND ls)

## file

    语句 : file(WRITE filename "message to write"... )
    作用 : WRITE选项将会写一条消息到名为filename的文件中。如果文件已经存在，该命令会覆盖已有的文件；如果文件不存在，它将创建该文件。

    ===========================================================

    语句 : file(APPEND filename "message to write"... )
    作用 : APPEND选项和WRITE选项一样，将会写一条消息到名为filename的文件中，只是该消息会附加到文件末尾。

    ===========================================================

    语句 : file(READ filename variable [LIMIT numBytes] [OFFSET offset] [HEX])
    作用 : READ选项将会读一个文件中的内容并将其存储在变量里。读文件的位置从offset开始，最多读numBytes个字节。如果指定了HEX参数，二进制代码将会转换为十六进制表达方式，并存储在变量里。

    ===========================================================

    语句 : file(STRINGS filename variable [LIMIT_COUNT num] [LIMIT_INPUT numBytes]  [LIMIT_OUTPUT numBytes]
                                                           [LENGTH_MINIMUM numBytes]   [LENGTH_MAXIMUM numBytes]
                                                            [NEWLINE_CONSUME] [REGEX regex]  [NO_HEX_CONVERSION])

    作用 : STRINGS将会从一个文件中将一个ASCII字符串的list解析出来，然后存储在variable变量中。文件中的二进制数据会被忽略。回车换行符会被忽略。它也可以用在Intel的Hex和Motorola的S-记录文件；读取它们时，它们会被自动转换为二进制格式。可以使用NO_HEX_CONVERSION选项禁止这项功能。LIMIT_COUNT选项设定了返回的字符串的最大数量。LIMIT_INPUT设置了从输入文件中读取的最大字节数。LIMIT_OUTPUT设置了在输出变量中存储的最大字节数。LENGTH_MINIMUM设置了要返回的字符串的最小长度；小于该长度的字符串会被忽略。LENGTH_MAXIMUM设置了返回字符串的最大长度；更长的字符串会被分割成不长于最大长度的字符串。NEWLINE_CONSUME选项允许新行被包含到字符串中，而不是终止它们。REGEX选项指定了一个待返回的字符串必须满足的正则表达式。
    ===========================================================

    语句 : file(GLOB variable [RELATIVE path] [globbing expressions]...)
    作用 : GLOB选项将会为所有匹配查询表达式的文件生成一个文件list，并将该list存储进变量variable里。文件名查询表达式与正则表达式类似，只不过更加简单。如果为一个表达式指定了RELATIVE标志，返回的结果将会是相对于给定路径的相对路径。
    ===========================================================

    语句 : file(GLOB_RECURSE variable [RELATIVE path] [FOLLOW_SYMLINKS] [globbing expressions]...)
    作用 : GLOB_RECURSE选项将会生成一个类似于通常的GLOB选项的list，只是它会寻访所有那些匹配目录的子路径并同时匹配查询表达式的文件。作为符号链接的子路径只有在给定FOLLOW_SYMLINKS选项或者cmake策略CMP0009被设置为NEW时，才会被寻访到。参见cmake --help-policy CMP0009 查询跟多有用的信息。
    ===========================================================

    语句 : file(RENAME <oldname> <newname>)
    作用 : RENAME选项对同一个文件系统下的一个文件或目录重命名。
    ===========================================================

    语句 : file(REMOVE [file1 ...])
    作用 : REMOVE选项将会删除指定的文件，包括在子路径下的文件。
    ===========================================================

    语句 : file(REMOVE_RECURSE [file1 ...])
    作用 : REMOVE_RECURSE选项会删除给定的文件以及目录，包括非空目录。
    ===========================================================

    语句 : file(MAKE_DIRECTORY [directory1 directory2 ...])
    作用 : MAKE_DIRECTORY选项将会创建指定的目录，如果它们的父目录不存在时，同样也会创建。（类似于mkdir命令——译注）
    ===========================================================

    语句 : file(RELATIVE_PATH variable directory file)
    作用 : RELATIVE_PATH选项会确定从direcroty参数到指定文件的相对路径。
    ===========================================================

    语句 : file(TO_CMAKE_PATH path result)
    作用 : TO_CMAKE_PATH选项会把path转换为一个以unix的 / 开头的cmake风格的路径。输入可以是一个单一的路径，也可以是一个系统路径，比如"$ENV{PATH}"。注意，在调用TO_CMAKE_PATH的ENV周围的双引号只能有一个参数(Note the double quotes around the ENV call TO_CMAKE_PATH only takes one argument. 原文如此。
    ===========================================================

    语句 : file(TO_NATIVE_PATH path result)
    作用 : TO_NATIVE_PATH选项与TO_CMAKE_PATH选项很相似，但是它会把cmake风格的路径转换为本地路径风格：windows下用\，而unix下用/。
    ===========================================================

    语句 : file(DOWNLOAD url file [TIMEOUT timeout] [STATUS status] [LOG log] [EXPECTED_MD5 sum] [SHOW_PROGRESS])
    作用 : DOWNLOAD 将给定的URL下载到指定的文件中。如果指定了LOG var选项，下载日志将会被输出到var中。如果指定了STATUS var选项，下载操作的状态会被输出到var中。该状态返回值是一个长度为2的list。list的第一个元素是操作的数字返回值，第二个返回值是错误的字符串值。错误信息如果是数字0，操作中没有发生错误。如果指定了TIMEOUT time选项，在time秒之后，操作会超时退出；time应该是整数。如果指定了EXPECTED_MD5 sum选项，下载操作会认证下载的文件的实际MD5和是否与期望值匹配。如果不匹配，操作将返回一个错误。如果指定了SHOW_PROGRESS选项，进度信息会以状态信息的形式被打印出来，直到操作完成。

## cmake 常用语句

### 条件控制

```bash
if(expression)
# ...
elseif(expression2)
    # ...
else()
    # ...
endif()
```

对于 if(string) 来说：
如果 string 为（不区分大小写）1、ON、YES、TRUE、Y、非 0 的数则表示真
如果 string 为（不区分大小写）0、OFF、NO、FALSE、N、IGNORE、空字符串、以 -NOTFOUND 结尾的字符串则表示假
如果 string 不符合上面两种情况，则 string 被认为是一个变量的名字。变量的值为第二条所述的各值则表示假，否则表示真

===========================================================

#### if 中的语句

- if(NOT expression) 为真的前提是 expression 为假
- if(expr1 AND expr2) 为真的前提是 expr1 和 expr2 都为真
- if(expr1 OR expr2) 为真的前提是 expr1 或者 expr2 为真
- if(COMMAND command-name) 为真的前提是存在 command-name 命令、宏或函数且能够被调用
- if(EXISTS name) 为真的前提是存在 name 的文件或者目录（应该使用绝对路径）
- if(file1 IS_NEWER_THAN file2) 为真的前提是 file1 比 file2 新或者 file1、file2 中有一个文件不存在（应该使用绝对路径）
- if(IS_DIRECTORY directory-name) 为真的前提是 directory-name 表示的是一个目录（应该使用绝对路径）
- if(variable|string MATCHES regex) 为真的前提是变量值或者字符串匹配 regex 正则表达式
- if(variable|string LESS variable|string)
  if(variable|string GREATER variable|string)
  if(variable|string EQUAL variable|string)
  为真的前提是变量值或者字符串为有效的数字且满足小于（大于、等于）的条件

- if(variable|string STRLESS variable|string)
  if(variable|string STRGREATER variable|string)
  if(variable|string STREQUAL variable|string)
  为真的前提是变量值或者字符串以字典序满足小于（大于、等于）的条件

- if(DEFINED variable) 为真的前提是 variable 表示的变量被定义了

#### 循环结构

##### foreach 循环

```bash
set(VAR a b c)
foreach(f ${VAR})
    message(${f})
endforeach()
```

##### while 循环

```bash
set(VAR 5)
while(${VAR} GREATER 0)
    message(${VAR})
    math(EXPR VAR "${VAR} - 1")
endwhile()
```

##### 宏定义

###### macro 循环

```bash
# 定义一个宏 hello
macro(hello MESSAGE)
    message(${MESSAGE})
endmacro()
# 调用宏 hello
hello("hello world")
# 定义一个函数 hello
function(hello MESSAGE)
    message(${MESSAGE})
endfunction()
```

###### 函数定义

```bash
function(get_func RESULT)
    # RESULT 的值为实参的值，因此需要使用 ${RESULT}
    # 这里使用 PARENT_SCOPE 是因为函数会构建一个局部作用域
    set(${RESULT} "Hello Function" PARENT_SCOPE)
endfunction()

macro(get_macro RESULT)
    set(${RESULT} "Hello Macro")
endmacro()

get_func(V1)
# 输出 Hello Function
message(${V1})
get_macro(V2)
# 输出 Hello Macro
message(${V2})
```

### 字符串控制

- string(REGEX MATCH (regular_expression) (output variable) (input) [(input)...])
- string(REGEX MATCHALL (regular_expression) (output variable) (input) [(input)...])
- string(REGEX REPLACE (regular_expression) (replace_expression) (output variable) (input) [(input)...])
- string(REPLACE (match_string) (replace_string) (output variable) (input) [(input)...])
- string(COMPARE EQUAL (string1) (string2) (output variable))
- string(COMPARE NOTEQUAL (string1) (string2) (output variable))
- string(COMPARE LESS (string1) (string2) (output variable))
- string(COMPARE GREATER (string1) (string2) (output variable))
- string(ASCII (number) [(number) ...] (output variable))
- string(CONFIGURE (string1) (output variable) [@ONLY][escape_quotes])
- string(TOUPPER (string1) (output variable))
- string(TOLOWER (string1) (output variable))
- string(LENGTH (string) (output variable))
- string(SUBSTRING (string) (begin) (length) (output variable))
- string(STRIP (string) (output variable))
- string(RANDOM [LENGTH (length)][alphabet (alphabet)] (output variable))

### cmake 常用变量

1. UNIX 如果为真，表示为 UNIX-like 的系统，包括 Apple OS X 和 CygWin
1. WIN32 如果为真，表示为 Windows 系统，包括 CygWin
1. APPLE 如果为真，表示为 Apple 系统
1. CMAKE_SIZEOF_VOID_P 表示 void\* 的大小（例如为 4 或者 8），可以使用其来判断当前构建为 32 位还是 64 位
1. CMAKE_CURRENT_LIST_DIR 表示正在处理的 CMakeLists.txt 文件的所在的目录的绝对路径（2.8.3 以及以后版本才支持）
1. CMAKE_ARCHIVE_OUTPUT_DIRECTORY 用于设置 ARCHIVE 目标的输出路径
1. CMAKE_LIBRARY_OUTPUT_DIRECTORY 用于设置 LIBRARY 目标的输出路径
1. CMAKE_RUNTIME_OUTPUT_DIRECTORY 用于设置 RUNTIME 目标的输出路径

#### 可能会用到的一些命令

##### get_property 获取一个属性值

get_property(<variable>
<GLOBAL |
DIRECTORY [dir] |
TARGET <target> |
SOURCE <source> |
TEST <test> |
CACHE <entry> |
VARIABLE>
PROPERTY <name>
[SET | DEFINED | BRIEF_DOCS | FULL_DOCS])

get_source_file_property 为一个源文件获取一种属性值
get_source_file_property(VAR file property)
get_target_property 从一个目标中获取一个属性值
get_target_property(VAR target property)
get_test_property 获取一个测试的属性
get_test_property(test VAR property)
get_cmake_property 获取一个 CMake 实例的属性
get_cmake_property(VAR property)
get_filename_component 得到一个完整文件名中的特定部分
get_filename_component(<VAR> FileName
PATH|ABSOLUTE|NAME|EXT|NAME_WE|REALPATH
[CACHE])

get_cmake_property 获取一个 CMake 实例的属性。
get_directory_property(<variable> [DIRECTORY <dir>] <prop-name>)

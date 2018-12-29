# Windows加载动态库的搜索路径问题

## 官方搜索路径

1. The directory from which the application loaded. （应用程序所在的目录）
1. The system directory. Use the GetSystemDirectory function to get the path of this directory. （system32目录）
1. The 16-bit system directory. There is no function that obtains the path of this directory, but it is searched. （System目录）
1. The Windows directory. Use the GetWindowsDirectory function to get the path of this directory. （Windows目录）
1. The current directory. （运行中的当前目录）
1. The directories that are listed in the PATH environment variable. Note that this does not include     the per-application path specified by the App Paths registry key. （PATH 路径）

## 简单总结一下简要的dll的加载顺序

- (1)EXE所在目录；
- (2)当前目录GetCurrentDirectory()；
- (3)系统目录GetSystemDirectory()；
- (4)WINDOWS目录GetWindowsDirectory()；
- (5)环境变量 PATH 所包含的目录。

所以使用loadlibrary加载dll使用的路径，但是这个函数会忽略这个路径，只会按既定规则加载dll。所以如果要加载指定目录的dll，可以用上述两个解决方案。
# 如何加载动态库？

Windows平台使用三个基本的函数可以加载动态库

先看源码 `WinBase.h` 文件：

```cpp
WINBASEAPI
__out_opt
HMODULE
WINAPI
LoadLibraryA(
    __in LPCSTR lpLibFileName
    );
WINBASEAPI
__out_opt
HMODULE
WINAPI
LoadLibraryW(
    __in LPCWSTR lpLibFileName
    );
#ifdef UNICODE
#define LoadLibrary  LoadLibraryW
#else
#define LoadLibrary  LoadLibraryA
#endif // !UNICODE
```


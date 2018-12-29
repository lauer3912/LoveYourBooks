# LoadLibrary 与 LoadLibraryW 与 LoadLibraryA 的区别

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

说明：

- （1）LoadLibrary 是动态来区分UNICODE和ANSI编码的动态库的
- （2）LoadLibraryA 是加载ANSI编码动态库的
- （3）LoadLibraryW 是加载UNICODE编码动态库的
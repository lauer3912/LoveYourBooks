# 加载动态库出错的错误编码，原因有哪些？

## 想知道加载动态库出现什么问题，可以先获得错误代码.

通过 `GetLastError()` 函数获取最后出错的代码编码

```cpp
DWORD dwError = 0;
hInstance = LoadLibrary(strDllName);
if(hInstance == NULL)
{
dwError = GetLastError();
return NULL;

}
```

## 出现问题的错误编码及解析

- 错误代码**126**：
# 资源和句柄

## 资源

Windows 中，经常用到的图标、光标、菜单、对话框等等，这些都是 Windows 的资源类型。
资源也是数据。

Windows 通过资源的处理，将资源与程序的许多组件链接编译到程序的.exe 文件中。

## 句柄 HANDLE

句柄是一个无符号的唯一整数值。用于标识应用程序中的各种对象、资源。如：窗口、光标、应用程序实例等等。

Windows 通过句柄来查找相应的对象、资源，用句柄来管理和操作对象和资源。

具体参照 《Windows 游戏编程》

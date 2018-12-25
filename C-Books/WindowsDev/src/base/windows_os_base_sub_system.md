# Windows 核心三个主要子系统

引用：《Windows 游戏编程》

Windows 核心主要部分仅仅通过三个动态链接库来实现。

krnl386.exe
kernel32.dll
user.exe
user32.dll
gdl.exe
gdl32.dll

1. Kernel: 处理所有在传统上由操作系统处理的事物，如：内存管理、文件 I/O 和多任务管理。
1. User: 使用者接口，实现所有窗口运作机制
1. GDL: 图形设备接口，允许程序在屏幕和打印机上显示文字和图形

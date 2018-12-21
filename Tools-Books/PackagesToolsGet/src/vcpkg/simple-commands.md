# 常用命令

## 在列表中搜索可用库

要查看哪些包可用，请在命令提示符中键入：vcpkg search

此命令枚举 vcpkg/ports 子文件夹中的控件文件。 将出现如下的文件列表：

```cmd
ace       6.4.3   The ADAPTIVE Communication Environment
anax      2.1.0-1 An open source C++ entity system. \<https://github...
antlr4    4.6-1   ANother Tool for Language Recognition
apr       1.5.2   The Apache Portable Runtime (APR) is a C library ...
asio      1.10.8  Asio is a cross-platform C++ library for network ...
assimp    3.3.1   The Open Asset import library
atk       2.24.0  GNOME Accessibility Toolkit
...
```

可以根据模式筛选，例如 vcpkg search ta：

```cmd
botan       2.0.1      A cryptography library written in C++11
portaudio   19.0.6.00  PortAudio Portable Cross-platform Audio I/O API P...
taglib      1.11.1-2   TagLib Audio Meta-Data Library
```

### 在本地计算机上安装库

在使用 vcpkg search 获取库的名称后，可使用 vcpkg install 下载库并对其进行编译。 vcpkg 在端口目录中使用库的端口文件。 如果未指定三元组，则 vcpkg 将针对目标平台的默认三元组进行安装和编译：x86-windows、x64-linux.cmake 或 x64-osx.cmake。

对于 Linux 库，vcpkg 取决于本地计算机上安装的 gcc。 在 MacOS 上，vcpkg 使用 Clang。

如果端口文件指定了依赖项，vcpkg 还会下载并安装这些依赖项。 下载完成后，vcpkg 使用库所使用的生成系统（版本不限）来生成库。 首选 CMake 和 MSBuild（Windows 上）项目，但同时还支持 MAKE 以及其他任何生成系统。 如果 vcpkg 在本地计算机上找不到指定的生成系统，它会下载并安装一个。

```cmd
> vcpkg install boost:x86-windows

The following packages will be built and installed:
    boost:x86-windows
  * bzip2:x86-windows
  * zlib:x86-windows
Additional packages (*) will be installed to complete this operation.
```

对于 CMAKE 项目，通过 CMAKE_TOOLCHAIN_FILE 来配合使用库和 `find_package()`。 例如:

```cmd
cmake .. -DCMAKE_TOOLCHAIN_FILE=vcpkg/scripts/buildsystems/vcpkg.cmake (Linux/MacOS)
cmake .. -DCMAKE_TOOLCHAIN_FILE=vcpkg\scripts\buildsystems\vcpkg.cmake (Windows)
```

## 列出已安装的库

在安装某些库以后，可使用 vcpkg list 来查看所获得的内容：

```cmd
> vcpkg list

boost:x86-windows       1.64-3   Peer-reviewed portable C++ source libraries
bzip2:x86-windows       1.0.6-1  High-quality data compressor.
cpprestsdk:x86-windows  2.9.0-2  C++11 JSON, REST, and OAuth library The C++ REST ...
openssl:x86-windows     1.0.2k-2 OpenSSL is an open source project that provides a...
websocketpp:x86-windows 0.7.0    Library that implements RFC6455 The WebSocket Pro...
zlib:x86-windows        1.2.11   A compression library
```

## 与 Visual Studio (Windows) 集成

### 按用户

运行 vcpkg integrate install 来配置 Visual Studio，以便按用户找到所有 vcpkg 头文件和二进制文件，同时还无需手动编辑 VC++ 目录路径。 如果有多个克隆，则运行此命令的克隆将成为新的默认位置。

现在，只需键入文件夹/标头就可轻松加入标头，自动完成功能将帮助你完成这一切。 在链接到 lib 或添加项目引用时，无需额外步骤。 下图演示了 Visual Studio 查找 azure-storage-cpp 标头的方法。 vcpkg 将其标头放置在 /installed 子文件夹中，由目标平台予以分区。 下图显示库的 /was 子文件夹中包含文件的列表：

![vcpkg IntelliSense 集成](https://docs.microsoft.com/zh-cn/cpp/media/vcpkg-intellisense.png?view=vs-2017 "vcpkg 和 IntelliSense")

### 按项目

如果需要使用的库的版本与活动 vcpkg 实例中的版本不同，请按以下步骤操作：

1. 新建 vcpkg 克隆
1. 修改库的端口文件以获取所需版本
1. 运行 vcpkg install \<library>。
1. 使用 vcpkg integrate project 创建 NuGet 包，它会按项目来引用该库。

## 与 Visual Studio Code (Linux/MacOS) 集成

运行 vcpkg integrate install，使用 vcpkg 登记的位置在 Linux/MacOS 上配置 Visual Studio Code，并在源文件上启用 IntelliSense。

## 通过 WSL 从 Windows 指向 Linux

可使用适用于 Linux 的 Windows 子系统 (WSL) 从 Windows 计算机生成 Linux 二进制文件。 按照说明[在 Windows 10 上设置 WSL](/windows/wsl/install-win10)，并使用[适用于 Linux 的 Visual Studio 扩展](https://blogs.msdn.microsoft.com/vcblog/2017/02/08/targeting-windows-subsystem-for-linux-from-visual-studio/)进行配置。 可将生成的所有 Windows 和 Linux 库放在同一文件夹中，并从 Windows 和 WSL 进行访问。

## 导出已编译的二进制文件和标头

让团队中的每个成员都去下载和生成库可能会造成效率低下。 一个团队成员就可完成该工作，然后使用 vcpkg export 创建二进制文件和标头的 zip 文件或 NuGet 包（各种格式均可），将其与其他团队成员进行轻松共享。

## 更新/升级已安装的库

公共目录始终与最新版本的库保持一致。 要判断哪个本地库已过期，请使用 vcpkg update。 准备好将端口集合更新为公共目录的最新版本后，运行 vcpkg upgrade 命令以自动下载和重新生成任一或所有已安装的过期库。

默认情况下，upgrade 命令仅列出过期库；而不会对它们进行升级。 要执行升级操作，请使用 --no-dry-run 选项。

```cmd
  vcpkg upgrade --no-dry-run
```

### 升级选项

- **--no-dry-run** 执行升级，在没有指定条件的情况下，命令只列出过期的包。
- **--keep-going** 继续安装包（即使出现了失败）。
- **--triplet \<t>** 为非限定的包设置默认的三元组。
- **--vcpkg-root \<path>** 指定要使用的 vcpkg 目录，而不是使用当前目录或工具目录。

### 升级示例

以下示例演示如何只升级指定的库。 请注意，必要时 vcpgk 会自动拉取依赖项。

```cmd
c:\users\satyan\vcpkg> vcpkg upgrade tiny-dnn:x86-windows zlib
The following packages are up-to-date:
   tiny-dnn:x86-windows

The following packages will be rebuilt:
    * libpng[core]:x86-windows
    * tiff[core]:x86-windows
      zlib[core]:x86-windows
Additional packages (*) will be modified to complete this operation.
If you are sure you want to rebuild the above packages, run this command with the --no-dry-run option.
```

## 发布新库

可以在自己的专用端口集合中添加任意库。 要建议适合公共目录的新库，请在 [GitHub vcpkg 问题页](https://github.com/Microsoft/vcpkg/issues)上打开一个问题。

## 删除库

键入 vcpkg remove 可删除已安装的库。 如果存在任何其他依赖于它的库，则系统会提示通过 --recurse 重新运行命令，如执行此操作，则下游的所有库都会被删除。

## 自定义 vcpkg

可凭自身喜好随意修改 vcpkg 的克隆。 可创建多个 vcpkg 克隆，修改每个克隆中的端口文件，使其包含特定版本的库或指定命令行参数。 例如在某企业中，某组的开发者可能正在使用拥有某一依赖项集的软件，而其他组可能拥有不同的集。 可设置两个 vcpkg 克隆并对其进行修改，以便根据需要来下载不同版本的库和编译开关等。

## 卸载 vcpkg

只需删除目录。

## 发送关于 vcpkg 反馈

使用 vcpkg contact --survey 命令向 Microsoft 发送关于 vcpkg 的反馈，包括 Bug 报告和功能上的建议。

## vcpkg 文件夹层次结构

所有 vcpkg 功能和数据都自包含在称为“实例”的单独目录层次结构中。 没有注册表设置或环境变量。 可以在计算机上设置任意数量的 vcpkg 实例，它们彼此互不干扰。

vcpkg 实例的内容如下：

- buildtrees - 包含从中生成每个库的源的子文件夹
- docs - 文档和示例
- downloads - 任何已下载工具或源的缓存副本。 运行安装命令时，vcpkg 会首先搜索此处。
- installed - 包含每个已安装库的标头和二进制文件。 与 Visual Studio 集成时，实质上相当于告知它将此文件夹添加到其搜索路径。
- packages - 在不同的安装之间用于暂存的内部文件夹。
- ports - 用于描述每个库的目录、版本和下载位置的文件。 如有需要，可添加自己的端口。
- scripts - 由 vcpkg 使用的脚本（cmake、powershell）。
- toolsrc - vcpkg 和相关组件的 C++ 源代码
- triplets - 包含每个受支持目标平台（如 x86-windows 或 x64-uwp）的设置。

## 命令行参考

| 命令                                         | 描述                                                |
| -------------------------------------------- | --------------------------------------------------- |
| **vcpkg search [pat]**                       | 搜索可安装的包                                      |
| **vcpkg install \<pkg>...**                  | 安装包                                              |
| **vcpkg remove \<pkg>...**                   | 卸载包                                              |
| **vcpkg remove --outdated**                  | 卸载所有过期包                                      |
| **vcpkg list**                               | 列出已安装的包                                      |
| **vcpkg update**                             | 显示用于更新的包列表                                |
| **vcpkg upgrade**                            | 重新生成所有过期包                                  |
| **vcpkg hash \<file> [alg]**                 | 通过特定算法对文件执行哈希操作，默认为 SHA512       |
| **vcpkg integrate install**                  | 使已安装包在用户范围内可用。 首次使用时需要管理权限 |
| **vcpkg integrate remove**                   | 删除用户范围的集成                                  |
| **vcpkg integrate project**                  | 为使用单个 VS 项目生成引用 NuGet 包                 |
| **vcpkg export \<pkg>... [opt]...**          | 导出包                                              |
| **vcpkg edit \<pkg>**                        | 打开端口进行编辑（使用 %EDITOR%，默认为“code”）     |
| **vcpkg create \<pkg> \<url> [archivename]** | 创建新程序包                                        |
| **vcpkg cache**                              | 列出缓存的已编译包                                  |
| **vcpkg version**                            | 显示版本信息                                        |
| **vcpkg contact --survey**                   | 显示联系信息，以便发送反馈。                        |

### 选项

| 选项                     | 描述                                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| **--triplet \<t>**       | 指定目标体系结构三元组。 （默认：`%VCPKG_DEFAULT_TRIPLET%`，另请参阅“vcpkg help triplet”） |
| **--vcpkg-root \<path>** | 指定 vcpkg 根目录（默认：`%VCPKG_ROOT%`）                                                  |

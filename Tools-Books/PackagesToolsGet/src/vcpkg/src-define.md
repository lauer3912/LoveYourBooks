---
title: vcpkg-- 用于 Windows、Linux 和 MacOS 的 C++ 包管理器
description: vcpkg 是一种命令行程序包管理器，可极大简化 Windows 上的开源 C++ 库的购置与安装。
author: mikeblome
ms.author: mblome
ms.date: 05/14/2018
ms.technology:
  - cpp-ide
ms.assetid: f50d459a-e18f-4b4e-814b-913e444cedd6
ms.openlocfilehash: 2f7dc6f1d9c78d894c5cf0e6ba20c8bdfc54e67a
ms.sourcegitcommit: afd6fac7c519dbc47a4befaece14a919d4e0a8a2
ms.translationtype: HT
ms.contentlocale: zh-CN
ms.lasthandoff: 11/10/2018
ms.locfileid: "51518679"
---

# <a name="vcpkg-a-c-package-manager-for-windows-linux-and-macos"></a>vcpkg：用于 Windows、Linux 和 MacOS 的 C++ 包管理器

vcpkg 是一种命令行包管理器，可极大简化 Windows、Linux 和 MacOS 上第三方库的购置与安装。 如果项目要使用第三方库，建议通过 vcpkg 来安装它们。 vcpkg 同时支持开源和专有库。 已测试 vcpkg Windows 目录中所有库与 Visual Studio 2015 及 Visual Studio 2017 的兼容性。 截至 2018 年 5 月，Windows 目录中已有 900 多个库，Linux/MacOS 目录中有 350 多个库。 C++ 社区正在不断向两个目录添加更多的库。

## <a name="simple-yet-flexible"></a>简单而灵活

仅通过单个命令就能下载源并生成库。 vcpkg 本身就是一个开源项目，可通过 GitHub 获取。 可凭喜好自定义个人专用克隆。 例如，除在公共目录中找到的内容外，还可指定不同的库或不同版本的库。 可在单台计算机上拥有多个 vcpkg 克隆，每个克隆都可生成自定义库集和/或编译开关等。每个克隆都是一个自包含、x 可复制的环境，它自身的 vcpkg.exe 副本仅可在自己的层次结构中运行。 vcpkg 不会被添加到任何环境变量，并且在 Windows 注册表或 Visual Studio 上也不会有依赖项。

## <a name="sources-not-binaries"></a>源不是二进制文件

对于 Windows 目录中的库，vcpkg 会下载源，而不是二进制文件[1]。 它将使用 Visual Studio 2017 或 Visual Studio 2015（如果未安装 Visual Studio 2017）对源进行编译。 在 C++ 中，作为链接到它的应用程序代码，使用相同的编译器及编译器版本来编译任何要用的库至关重要。 通过 vcpkg 可以消除或最大程度减少不匹配二进制文件的存在风险及它可能造成的问题。 对于使用特定编译器版本的标准化团队，可让一位成员使用 vcpkg 下载源并编译一组二进制文件，然后通过导出命令将二进制文件和标头压缩打包，即可与其他团队成员进行共享。 有关详细信息，请参阅下方的[导出已编译二进制文件及标头](#export_binaries_per_project)。

如果在端口集合中使用专用库创建 vcpkg 克隆，则可以添加一个端口来下载预生成二进制文件和标头，并编写一个 portfile.cmake 文件，轻松将上述文件复制到所需的地方。

[1] 注意：某些专有库不具有这些源。在这些情况下，vcpkg 将下载可兼容预生成二进制文件。\*

## <a name="installation"></a>安装

从 GitHub 克隆 vcpkg 存储库： https://github.com/Microsoft/vcpkg. 可凭喜好下载到任意文件夹位置。

在根文件夹中运行 bootstrapper：

- **bootstrap-vcpkg.bat** (Windows)
- **./bootstrap-vcpkg.sh** (Linux、MacOS)

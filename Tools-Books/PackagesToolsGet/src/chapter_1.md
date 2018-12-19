# Choco

The package manager for Windows
Chocolatey - Software Management Automation

网址：[https://chocolatey.org](https://chocolatey.org)

Welcome to the Chocolatey Community Package Repository! The packages found in this section of the site are provided, maintained, and moderated by the community.

欢迎来到Chocolatey社区包存储库！网站此部分中的软件包由社区提供，维护和审核。

## 特点

- Security, consistency, and quality checking 安全性、一致性和质量检查
- Installation testing 经过安装测试过
- Virus checking through VirusTotal 通过了VirusTotal检查病毒
- Human moderators who give final review and sign off 最终通过审核并由负责人签字

## 如何安装？

1. First, ensure that you are using an administrative shell - you can also install as a non-admin, check out Non-Administrative Installation.
1. Copy the text specific to your command shell - cmd.exe or powershell.exe.
1. Paste the copied text into your shell and press Enter.
1. Wait a few seconds for the command to complete.
1. If you don't see any errors, you are ready to use Chocolatey! Type choco or choco -? now, or see Getting Started for usage instructions.

```cmd
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
```

## 全局设置系统环境变量

```cmd
SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
```

> 需要通过 "系统高级设置" -> "环境变量"  -> 添加到系统环境变量中
> 然后，重新启动shell就可以使用了。

## 如何更新该工具 ?

```cmd
choco upgrade chocolatey
```

## 如何安装 "包" ?

```cmd
choco install firacode
```

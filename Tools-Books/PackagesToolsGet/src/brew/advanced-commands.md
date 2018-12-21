# 命令行高级功能

```bash
brew --version
brew command [--verbose|-v] [options] [formula] …
```

更多信息可以参考 [https://docs.brew.sh/Manpage](https://docs.brew.sh/Manpage)

| 命令                                                             | 描述                                                   |
| ---------------------------------------------------------------- | ------------------------------------------------------ |
| **brew analytics [state]**                                       | 显示匿名用户行为分析状态                               |
| **brew analytics (on\|off)**                                     | 关闭或开启 Homebrew 的分析                             |
| **brew analytics regenerate-uuid**                               | 重新生成 Homebrew 分析中使用的 UUID                    |
| **brew cat FORMULA...**                                          | 显示 FORMULA 的源                                      |
| **brew cleanup [--prune=days][--dry-run] [-s][formulae\|casks]** |                                                        |
| **brew command [cmd]**                                           | 显示调用 brew cmd 时使用的文件路径。                   |
| **brew commands [--quiet [--include-aliases]]**                  | 显示内置和外部命令的列表。                             |
| **brew config**                                                  | 显示 Homebrew 和系统配置对调试很有用。                 |
| **brew deps ...**                                                | 显示公式的依赖项。                                     |
| **brew desc formula ...**                                        | 显示公式的名称和单行描述。                             |
| **brew diy ...**                                                 | 自动确定非自制软件的安装前缀。                         |
| **brew fetch ...**                                               | 下载给定公式的源包。                                   |
| **brew gist-logs ...**                                           | 下将失败的公式构建的日志上载到新 Gist                  |
| **brew home**                                                    | 在浏览器中打开 Homebrew 自己的主页                     |
| **brew home formula**                                            | 在浏览器中打开公式的主页。                             |
| **brew info**                                                    | 显示 Homebrew 安装的简要统计信息。                     |
| **brew info ...**                                                | 显示有关公式和分析数据的信息                           |
| **brew install ...**                                             | 更多关于安装公式的参数                                 |
| **brew leaves**                                                  | 显示不是另一个已安装公式的依赖项的已安装公式           |
| **brew ln, link**                                                | 已安装文件符号链接到 Homebrew 前缀中                   |
| **brew list, ls**                                                | 列出所有已安装的公式                                   |
| **brew log ...**                                                 | 显示给定公式的 git 日志                                |
| **brew migrate ...**                                             | 将重命名的包迁移到新名称                               |
| **brew missing ...**                                             | 检查给定的公式是否缺少依赖项。                         |
| **brew options ...**                                             | 显示特定于公式的安装选项。                             |
| **brew outdated ...**                                            | 显示具有更新版本的公式。                               |
| **brew pin ...**                                                 | 固定挂起指定的公式。不参与更新                         |
| **brew postinstall ...**                                         | 重新运行公式的安装后步骤。                             |
| **brew prune ...**                                               | 从 Homebrew 前缀中删除死符号链接。                     |
| **brew readall ...**                                             | 从指定的 taps 导入所有公式                             |
| **brew reinstall ...**                                           | 重新安装公式                                           |
| **brew search, -S ...**                                          | 显示所有本地可用的公式                                 |
| **brew sh [--env=std] ...**                                      | 启动 Homebrew 构建环境 shell                           |
| **brew shellenv ...**                                            | 打印 shell 环境变量                                    |
| **brew style ...**                                               | 检查公式或文件是否符合 Homebrew 样式指南               |
| **brew style ...**                                               | 检查公式或文件是否符合 Homebrew 样式指南               |
| **brew switch formula version ...**                              | 符号链接特定版本的公式                                 |
| **brew tap ...**                                                 | 列出所有已安装 Taps                                    |
| **brew tap-info ...**                                            | 显示所有已安装的 Tap 的简短摘要                        |
| **brew tap-pin ...**                                             | 固定挂起已安装的 tap                                   |
| **brew tap-unpin ...**                                           | 解除固定挂起已安装的 tap                               |
| **brew uninstall, rm, remove ...**                               | 卸载或者删除公式                                       |
| **brew unlink ...**                                              | 从 Homebrew 前缀中删除公式的符号链接                   |
| **brew unpack ...**                                              | 将公式的源文件解压缩到当前工作目录的子目录中           |
| **brew unpin ...**                                               | 解除固定挂起已安装的公式                               |
| **brew untap tap**                                               | 删除一个 tapped 存储库。                               |
| **brew update ...**                                              | 更新 HomeBrew 所有的公式信息                           |
| **brew update-reset ...**                                        | 更新及重置 HomeBrew 所有的公式信息                     |
| **brew upgrade ...**                                             | 更新过期的非固定的公式                                 |
| **brew uses ...**                                                | 显示将公式指定为依赖项的公式                           |
| **brew --cache ...**                                             | 显示 Homebrew 下载的缓存。HOMEBREW_CACHE               |
| **brew --cellar ...**                                            | 显示 Homebrew 的 Cellar 路径。\$(brew --prefix)/Cellar |
| **brew --env ...**                                               | 显示 Homebrew 的 构建环境                              |
| **brew --prefix ...**                                            | 显示 Homebrew 的 路径前缀                              |
| **brew --repository ...**                                        | 显示 Homebrew 的 包含.git 根路径                       |
| **brew --version ...**                                           | 显示 Homebrew 的 版本信息                              |
|                                                                  |                                                        |

更多信息可以参考 [https://docs.brew.sh/Manpage](https://docs.brew.sh/Manpage)

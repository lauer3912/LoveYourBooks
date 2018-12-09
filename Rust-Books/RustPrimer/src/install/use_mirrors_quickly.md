# 利用科大镜像源提速

Rust感觉是被墙损伤最大的一门开发语言，中科大源支持Rust，实在是美的很！ 废话不多说,直接上教程！

## 配置`rustup`

``` shell
vi ~/.bashrc
```

然后加入：`RUSTUP_DIST_SERVER` 与 `RUSTUP_UPDATE_ROOT` 这两个环境变量

``` shell
export RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static
export RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup
```

接下来，使其环境变量生效!

``` shell
source ~/.bashrc
```

然后，你可以直接使用 `curl` 来下载你想要的版本. { nightly 日构建版本； stable 稳定发布版 本 }

``` shell
curl -sSf https://mirrors.ustc.edu.cn/rust-static/rustup.sh | sh -s -- --channel=nightly
```

当然，也可以直接访问 `https://mirrors.ustc.edu.cn/rust-static` 下载安装镜像。以上这么做，是为了以后执行有关 Rust 升级或者添加组件的时候，都从镜像源站点下载。

# 配置`cargo`

检查一下，`~/.cargo/` 是否存在？ 如果不存在，创建目录并新建一个`config`文件

``` shell
mkdir -R ~/.cargo/ && cd ~/.cargo/ && touch config
```

然后 `vi config`, 在里面填入以下内容：

``` toml

[registry]
index = "https://mirrors.ustc.edu.cn/crates.io-index/"

[source.crates-io]
registry = "https://github.com/rust-lang/crates.io-index"
replace-with = 'ustc'

[source.ustc]
registry = "https://mirrors.ustc.edu.cn/crates.io-index/"

```

这样，以后使用 `cargo install` 命令安装其他包装就非常方便了。
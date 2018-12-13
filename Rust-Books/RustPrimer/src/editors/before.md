# 前期准备

## 下载 Rust 源代码（供 racer 使用）

### 从github下载

`git clone https://github.com/rust-lang/rust.git`

### 从官网下载源代码包

下载地址： `https://static.rust-lang.org/dist/rustc-nightly-src.tar.gz`

### 使用rustup下载（推荐）

使用rustup获取源码最大的好处在于可以使用`rustup update`随时获取最新版源码，执行以下命令获取源码

```bash
rustup component add rust-src
```

## racer

racer是一个由rust的爱好者提供的rust自动补全和语法分析工具，被用来提供基本的补全功能和定义跳转功能。其本身完全由rust写成，补全功能已经比较完善了。

我们可以通过如下的方式获取它：

### cargo自动安装

在rust 1.5版本以后，其安装包自带的cargo工具已经支持了cargo install命令，这个命令可以帮助我们通过简单的方式获取到`racer`的最新版。

你可以通过以下命令安装`racer`最新版，目前已知在Linux、Unix和Windows上适用

```bash
cargo install racer
```

### 编译安装

事实上我更推荐有条件的用户通过这种方式安装，因为自己实战操作一遍总是有些收获的。~~(帅气可爱的DCjanus表示怀疑)~~

#### 下载源码

首先，我们需要下载racer的源码

```bash
git clone https://github.com/phildawes/racer.git
```

#### 进行编译

然后，进入目录然后进行编译

```bash
cd racer && cargo build --release
```

这样，我们会得到racer的二进制文件在 `target/release/racer`目录

#### 设置环境变量

为了对Rust标准库进行补全，racer需要获取Rust源码路径。

设置名为`RUST_SRC_PATH`的环境变量为`[path_to_your_rust_source]/src`

其中`[path_to_your_rust_source]`表示源码所在文件夹，使用rustup获取Rust源码的情况下`[path_to_your_rust_source]`默认为`~/.multirust/toolchains/[your-toolchain]/lib/rustlib/src/rust/src`

### 测试

请重新打开终端，并进入到关闭之前的路径。
执行如下代码：
linux:

```bash
./target/release/racer complete std::io::B
```

windows:

```bash
target\release\racer complete std::io::B
```

你将会看到racer的提示，这表示racer已经执行完成了。

## 安装 rustfmt

`cargo install rustfmt`

## Rust Langular Server (RLS)

`Rust Langular Server`(下文简称`RLS`)可以为很多IDE或编辑器提供包括不限于自动补全、跳转定义、重命名、跳转类型的功能支持。

使用rustup安装步骤如下:

1. 保证`rustup`为最新版。关于
    ```bash
    rustup self update
    ```
    关于 `rustup` 的用法，参照： [https://github.com/rust-lang/rustup.rs](https://github.com/rust-lang/rustup.rs)
2. [可选]升级工具链(并不要求设置`nightly`为默认，但需要保证安装了`nightly`工具链)
    ```bash
    rustup update nightly
    ```
3. [可选]正式安装RLS 的 nightly方式
    ```bash
    rustup component add rls --toolchain nightly
    rustup component add rust-analysis --toolchain nightly
    rustup component add rust-src --toolchain nightly
    rustup component add clippy-preview
    ```
4. 设置环境变量
    如果在安装Racer时没有设置名为`RUST_SRC_PATH`的环境变量，请参考前文进行设置。

**该项目托管地址:[https://github.com/rust-lang-nursery/rls](https://github.com/rust-lang-nursery/rls)**

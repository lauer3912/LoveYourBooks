# Rust Programming Language Primer - Rust 编程语言入门

此存储库包含所有版本的 《Rust Programming Language Primer - Rust 编程语言入门》

## 准备

构建该电子书需要先安装 [mdBook], 可以参照[rust-lang/rust uses in this file][rust-mdbook].

[mdBook]: https://github.com/azerupi/mdBook
[rust-mdbook]: https://github.com/rust-lang/rust/blob/master/src/tools/rustbook/Cargo.toml

```bash
$ cargo install mdbook --vers [version-num]
```

## 构建

构建电子书，需要使用 `cd` 命令到你想建立书的目录, 然后使用 `mdbook build` 命令来构建生成。

```bash
$ cd ~/RustBooks/RustPrimer/
$ mdbook build
```

构建的输出一般在 `book` 子目录中，你可以在浏览器中查看该电子书的样式、内容。

打开相应的浏览器方法如下：

_Firefox:_
```bash
$ firefox book/index.html                       # Linux
$ open -a "Firefox" book/index.html             # OS X
$ Start-Process "firefox.exe" ./book/index.html # Windows (PowerShell)
$ start firefox.exe ./book/index.html           # Windows (Cmd)
```

_Chrome:_
```bash
$ google-chrome book/index.html                 # Linux
$ open -a "Google Chrome" book/index.html       # OS X
$ Start-Process "chrome.exe" ./book/index.html  # Windows (PowerShell)
$ start chrome.exe ./book/index.html            # Windows (Cmd)
```

 `mdbook` 的帮助文档可以在[官方网站](https://rust-lang-nursery.github.io/mdBook/)找到。

下面是常用的方法：

- `mdbook init`

    The init command will create a directory with the minimal boilerplate to
    start with.

    ```text
    book-test/
    ├── book
    └── src
        ├── chapter_1.md
        └── SUMMARY.md
    ```

    `book` and `src` are both directories. `src` contains the markdown files
    that will be used to render the output to the `book` directory.

    Please, take a look at the [CLI docs] for more information and some neat tricks.

- `mdbook build`

    This is the command you will run to render your book, it reads the
    `SUMMARY.md` file to understand the structure of your book, takes the
    markdown files in the source directory as input and outputs static html
    pages that you can upload to a server.

- `mdbook watch`

    When you run this command, mdbook will watch your markdown files to rebuild
    the book on every change. This avoids having to come back to the terminal
    to type `mdbook build` over and over again.

- `mdbook serve`

    Does the same thing as `mdbook watch` but additionally serves the book at
    `http://localhost:3000` (port is changeable) and reloads the browser when a
    change occurs.

- `mdbook clean`

    Delete directory in which generated book is located.

本书使用 `CC BY-SA 4.0` 协议。
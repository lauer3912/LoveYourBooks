# extern crate 的用途

用途：用来定义加载外部模块，也可以称为 “加载外部 crate”

前面我们讲的，都是在当前 crate 中的技术。真正我们在开发时，会大量用到外部库。外部库是通过

```rust
extern crate xxx;
```

这样来引入的。

注：要使上述引用生效，还必须在 `Cargo.toml` 的 `dependecies` 段，加上 `xxx="version num"` 这种依赖说明，详情见 `Cargo 项目管理` 这一章。

引入后，就相当于引入了一个符号 `xxx`，后面可以直接以这个 `xxx` 为根引用这个 crate 中的 item：

```rust
extern crate xxx;

use xxx::yyy::zzz;
```

引入的时候，可以通过 `as` 关键字重命名。

```rust
extern crate xxx as foo;

use foo::yyy::zzz;
```
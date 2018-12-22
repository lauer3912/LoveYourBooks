# Eigen 数学库

## 网址

[https://arma.sourceforge.net/](https://arma.sourceforge.net/)

## 在线文档

[http://arma.sourceforge.net/docs.html](http://arma.sourceforge.net/docs.html)

## 安装

```bash
brew install armadillo
```

## 使用

```c
# CMakeLists.txt 文件中的使用

# Use brew? or use vcpkg?
set(UD_USE_VCPKG false)
set(UD_USE_BREW true)

if(${UD_USE_BREW})
    set(ARMADILLO_LIBRARY "$(brew --prefix armadillo)/lib")
    set(ARMADILLO_INCLUDE_DIR "$(brew --prefix armadillo)/include")
endif()
```

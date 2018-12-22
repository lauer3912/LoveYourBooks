# C/C++与 CMake

## \$(brew --prefix 库的名称) 获取库的路径

CMakeLists.txt 文件中，可以这样使用

```c
# 添加第三方数学库armadillo
# 设置armadillo的include及lib路径
if(${UD_USE_BREW})
    set(ARMADILLO_LIBRARY "$(brew --prefix armadillo)/lib")
    set(ARMADILLO_INCLUDE_DIR "$(brew --prefix armadillo)/include")
endif()
# 告知依赖 armadillo 库
find_package(armadillo REQUIRED)
```

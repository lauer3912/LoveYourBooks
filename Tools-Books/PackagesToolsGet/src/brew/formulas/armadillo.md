# armadillo 数学库

Armadillo 是一个用于 C ++语言的高质量线性代数库（矩阵数学），旨在实现速度和易用性之间的良好平衡

1. Armadillo is a high quality linear algebra library (matrix maths) for the C++ language, aiming towards a good balance between speed and ease of use
1. Provides high-level syntax and functionality deliberately similar to Matlab
1. Useful for algorithm development directly in C++, or quick conversion of research code into production environments (eg. software & hardware products)
1. Provides efficient classes for vectors, matrices and cubes (1st, 2nd and 3rd order tensors); dense and sparse matrices are supported
1. Integer, floating point and complex numbers are supported
1. Various matrix decompositions are provided through integration with LAPACK, or one of its high performance drop-in replacements (eg. multi-threaded Intel MKL, or OpenBLAS)
1. A sophisticated expression evaluator (based on template meta-programming) automatically combines several operations to increase speed and efficiency
1. Can automatically use OpenMP multi-threading (parallelisation) to speed up computationally expensive operations
1. Available under a permissive license, useful for both open-source and proprietary (closed-source) software
1. Can be used for machine learning, pattern recognition, computer vision, signal processing, bioinformatics, statistics, finance, etc

---

1. 提供与 Matlab 类似的高级语法和功能.
1. 可用于直接在 C++中进行算法开发，或将研究代码快速转换为生产环境（例如，软件和硬件产品）
1. 为向量，矩阵和立方体（一阶，二阶和三阶张量）提供有效的类;支持密集和稀疏矩阵
1. 支持整数，浮点数和复数
1. 通过与 LAPACK 集成或其高性能直接替换之一（例如，多线程英特尔 MKL 或 OpenBLAS）提供各种矩阵分解
1. 复杂的表达式评估程序（基于模板元编程）自动组合多个操作以提高速度和效率
1. 可以自动使用 OpenMP 多线程（并行化）来加速计算上昂贵的操作
1. 在许可许可下可用，对开源和专有（闭源）软件都很有用
1. 可用于机器学习，模式识别，计算机视觉，信号处理，生物信息学，统计学，金融学等

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

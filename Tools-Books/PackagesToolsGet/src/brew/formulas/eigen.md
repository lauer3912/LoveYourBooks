# Eigen 数学库

## 网址

[http://eigen.tuxfamily.org/](http://eigen.tuxfamily.org/)

## 在线文档

[http://eigen.tuxfamily.org/index.php?title=Main_Page](http://eigen.tuxfamily.org/index.php?title=Main_Page)

## 说明

非常强大的矩阵运算库，我一直在用，大家用了都说好。使用类似 Matlab 的方式操作矩阵，可以在这里查看官方的与 Maltab 的对应关系，个人感觉单纯讲和 Matlab 的对应的话，可能不如 Armadillo 对应的好，但功能绝对强大。Eigen 包含了绝大部分你能用到的矩阵算法，同时提供许多第三方的接口。Eigen 一个重要特点是没有什么依赖的库，本身仅有许多头文件组成，因此非常轻量而易于跨平台。你要做的就是把用到的头文件和你的代码放在一起就可以了。Eigen 的一些特性：

- 支持整数、浮点数、复数，使用模板编程，可以为特殊的数据结构提供矩阵操作。比如在用 ceres-solver 进行做优化问题（比如 bundle adjustment）的时候，有时候需要用模板编程写一个目标函数，ceres 可以将模板自动替换为内部的一个可以自动求微分的特殊的 double 类型。而如果要在这个模板函数中进行矩阵计算，使用 Eigen 就会非常方便。
- 支持逐元素、分块、和整体的矩阵操作。
- 内含大量矩阵分解算法包括 LU，LDLt，QR、SVD 等等。
- 支持使用 Intel MKL 加速
- 部分功能支持多线程
- 稀疏矩阵支持良好，到今年新出的 Eigen3.2，已经自带了 SparseLU、SparseQR、共轭梯度（ConjugateGradient solver）、bi conjugate gradient stabilized solver 等解稀疏矩阵的功能。同时提供 SPQR、UmfPack 等外部稀疏矩阵库的接口。
- 支持常用几何运算，包括旋转矩阵、四元数、矩阵变换、AngleAxis（欧拉角与 Rodrigues 变换）等等。
- 更新活跃，用户众多（Google、WilliowGarage 也在用），使用 Eigen 的比较著名的开源项目有 ROS（机器人操作系统）、PCL（点云处理库）、Google Ceres（优化算法）。OpenCV 自带到 Eigen 的接口。

总体来讲，如果经常做一些比较复杂的矩阵计算的话，或者想要跨平台的话，非常值得一用。

## 安装

```bash
brew install eigen
```

## CMakeLists.txt 使用

```c
# CMakeLists.txt 文件中的使用

# Use brew? or use vcpkg?
set(UD_USE_VCPKG false)
set(UD_USE_BREW true)

if(${UD_USE_BREW})
    # About eigen (http://eigen.tuxfamily.org)
    # Eigen is a pure template library defined in the headers
    # If you just want to use Eigen, you can use the header files right away.
    # There is no binary library to link to, and no configured header file.
    set(EIGEN_INCLUDE_DIR "$(brew --prefix eigen)/include")
endif()
```

## 实例

```c
#include <iostream>
#include <eigen3/Eigen/Dense>
```

```c
    // 下面是基础的线性代数组解法
    Eigen::Matrix3f A;
    A << 1,1,1, 0,2,5 , 2,5,-1;
    Eigen::Vector3f B;
    B << 6, -4, 27;
    std::cout << "Here is the matrix A:\n" << A << std::endl;
    std::cout << "Here is the vector b:\n" << B << std::endl;
    Eigen::Vector3f x = A.colPivHouseholderQr().solve(B);
    std::cout << "The solution is:\n" << x << std::endl;

//    Here is the matrix A:
//    1  1  1
//    0  2  5
//    2  5 -1
//    Here is the vector b:
//    6
//    -4
//    27
//    The solution is:
//    5
//    3
//    -2
```

# PETSc 数学库

## 网址

[http://www.mcs.anl.gov/petsc/](http://www.mcs.anl.gov/petsc/)

## 在线文档

[http://eigen.tuxfamily.org/index.php?title=Main_Page](http://eigen.tuxfamily.org/index.php?title=Main_Page)

## 说明

许可证：Copyright University of Chicago (GPL compatible)

PETSc(Portable, Extensible Toolkit for Scientific Computation) 是美国能源部 ODE2000 支持开发的 20 多个 ACTS 工具箱之一，由 Argonne 国家实验室开发的可移植可扩展科学计算工具箱，主要用于在分布式存储环境高效求解偏微分方程组及相关问题。PETSc 所有消息传递通信均采用 MPI 标准实现。线性方程组求解器是 PETSc 的核心组件之一，PETSc 几乎提供了所有求解线性方程组的高效求解器，既有串行求解也有并行求解，既有直接法求解也有迭代法求解。对于大规模线性方程组， PETSc 提供了大量基于 Krylov 子空间方法和各种预条件子的成熟而有效的迭代方法，以及其他通用程序和用户程序的接口。PETSc 具有一般库软件所具备的高性能、可移植等优点，而且面向对象技术使得 PETSc 内部功能部件的使用非常方便，接口简单而又适用面广，可以缩短开发周期，减少工作量。。

PETSc 在网上可一找到很多英文资料，使用也比较广泛。不过在学校实验室的一般的科学计算可能接触的还比较少。推荐一个 YouTube（可能要翻墙）的五集 PETSc 简单入门[《PRACE Video Tutorial – PETSc Tutorial》](http://www.youtube.com/watch?v=ubp_cSibb9I)。

## 安装

```bash
brew install petsc
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

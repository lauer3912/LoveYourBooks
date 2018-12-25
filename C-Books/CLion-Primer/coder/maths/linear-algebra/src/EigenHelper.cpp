//
// Created by ian on 2018-12-21.
//
#include "EigenHelper.h"

#include <iostream>
#include <eigen3/Eigen/Dense>

using Eigen::MatrixXd;

void fmt(const char * content) {
    std::cout << content <<  std::endl;
}

void linearAlgebraDemo() {
    fmt("求解：线性方程组的解");
    fmt("（1） x + y + z = 6");    /// 1, 1, 1
    fmt("（2） 2y + 5z = -4");     /// 0, 2, 5
    fmt("（3） 2x + 5y - z = 27"); /// 2, 5, -1
    fmt("求解：x，y，z 的值");


    // 下面是基础的线性代数组解法
    Eigen::Matrix3f A;
    A << 1,1,1, 0,2,5 , 2,5,-1;
    Eigen::Vector3f B;
    B << 6, -4, 27;
    std::cout << "矩阵 A:\n" << A << std::endl;
    std::cout << "矩阵 B:\n" << B << std::endl;
    Eigen::Vector3f x = A.colPivHouseholderQr().solve(B);
    std::cout << "线性代数组的解:\n" << x << std::endl;
}

void EigenHelper::RunTest() {
    linearAlgebraDemo();
}

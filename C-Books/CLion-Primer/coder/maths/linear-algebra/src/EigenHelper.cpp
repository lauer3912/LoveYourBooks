//
// Created by ian on 2018-12-21.
//
#include "EigenHelper.h"

#include <iostream>
#include <eigen3/Eigen/Dense>

using Eigen::MatrixXd;

void EigenHelper::RunTest() {
    std::cout << "Hi" << std::endl;

    MatrixXd m(2, 2);
    m(0, 0) = 3;
    m(1, 0) = 2.5;
    m(0, 1) = -1;
    m(1, 1) = m(1, 0) + m(0, 1);
    std::cout << m << std::endl;

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
}

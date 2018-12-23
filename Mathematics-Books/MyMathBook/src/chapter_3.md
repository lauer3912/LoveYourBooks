# Linear Algebra 线性代数方程组

关于这方面的内容，请参考《线性代数及其应用》原书第 3 版，(美) David C. Lay 编写。

## Python 中实际的计算方式

1. [SageMath](http://www.sagemath.org) **“这款开源软件的支持者称 Sage 能够完成从 12 维物体到计算全球变暖效应数学模型中的降雨量的任何事情。”Sage 包含了从线性代数、微积分，到密码学、数值计算、组合数学、群论、图论、数论等各种初高等数学的计算功能。**
1. numpy && scipy

```python
from scipy import linalg
import numpy as np

def main():
    '''
    线性代数方程组：
    （1） x + y + z = 6
    （2） 2y + 5z = -4
    （3） 2x + 5y - z = 27
    求解：
    '''
    A = np.array([[1,  1,  1],  [0,  2,  5], [2,  5,  -1]])
    B = np.array([6, -4, 27])
    x = linalg.solve(A, B)
    print(x)

if __name__ == '__main__':
    main()
```

## Rust

## Go

## C++ 利用第三方库计算方式

C++ 可以使用的第三方库来计算，一般有如下几种：

1. [PETSc](http://www.mcs.anl.gov/petsc/) **大规模并行科学计算**
1. [OpenCV](http://opencv.org/) **方便的计算机视觉计算库**
1. [Armadillo](https://arma.sourceforge.net) **for linear algebra & scientific computing C++下的 Matlab 替代品**

   ```c++

   ```

1. [Eigen](https://eigen.tuxfamily.org) **for Dense matrix and array manipulations and sparse linear algebra 强大且只需头文件**

   ```c++
       // 下面是基础的线性代数组解法
   Eigen::Matrix3f A;
   A << 1,1,1, 0,2,5 , 2,5,-1;
   Eigen::Vector3f B;
   B << 6, -4, 27;
   std::cout << "Here is the matrix A:\n" << A << std::endl;
   std::cout << "Here is the vector b:\n" << B << std::endl;
   Eigen::Vector3f x = A.colPivHouseholderQr().solve(B);
   std::cout << "The solution is:\n" << x << std::endl;
   ```

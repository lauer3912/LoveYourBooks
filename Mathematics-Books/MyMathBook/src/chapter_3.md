# Linear Algebra 线性代数方程组

关于这方面的内容，请参考《线性代数及其应用》原书第 3 版，(美) David C. Lay 编写。

## Python 中实际的计算方式

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

## C++ 利用第三方库计算方式

C++ 可以使用的第三方库来计算，一般有如下几种：

1. [Armadillo](https://arma.sourceforge.net) **for linear algebra & scientific computing**
1. [Eigen](https://eigen.tuxfamily.org) **for Dense matrix and array manipulations and sparse linear algebra**

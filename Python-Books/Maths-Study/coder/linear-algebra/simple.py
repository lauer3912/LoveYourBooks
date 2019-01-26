import numpy as np
from scipy import linalg


def main():
    '''
    线性代数方程组：
    （1） x + y + z = 6
    （2） 2y + 5z = -4
    （3） 2x + 5y - z = 27
    求解：
    '''

    A = np.array([[1, 1, 1], [0, 2, 5], [2, 5, -1]])
    B = np.array([6, -4, 27])
    x = linalg.solve(A, B)
    print(x)


if __name__ == '__main__':
    main()

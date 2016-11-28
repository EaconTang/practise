from numpy import *

if __name__ == '__main__':
    mat = mat(random.rand(4, 4))
    mat_inv = mat.I
    print mat * mat_inv - eye(4)

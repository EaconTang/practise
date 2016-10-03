# coding=utf-8
# 汉诺塔思想：将n个盘子由a移到b，借助中介m；n>1的话，先把a上的n－1个移到m，再把剩下的一个移到b；再把m上的n－1个移回b；递归

def han(n, a, b, m):
    if n == 1:
        print a, '->', b
    else:
        han(n - 1, a, m, b)
        print a, '->', b
        han(n - 1, m, b, a)


if __name__ == '__main__':
    han(5, '左', '右', '中')

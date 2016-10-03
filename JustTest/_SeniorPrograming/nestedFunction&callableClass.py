# coding:utf-8
'''
如何使用python中更高阶的函数?
有两个选择：你可以使用内嵌的方式或使用可调用对象。
'''


def result(a, b):
    def xResult(x):
        return x * (a + b)

    return xResult


print type(result(1, 1))  # <type 'function'>
f = result(1, 1)  # f = nestedF(x) =  x*(1+1)
print f

print f(3)  # 6


class Result:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, x):
        '''
        called by new a class object
        :param x:
        :return: f(x) = x*(a+b)
        '''
        return x * (self.a + self.b)


objResult = Result(1, 2)
print objResult  # Result instance;a function:f(x)=x*(1+2)
print objResult(4)  # 12

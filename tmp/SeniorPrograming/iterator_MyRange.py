#coding=utf-8
"""
重载__iter__方法，结合yield实现迭代器
"""

class MyRange:
    def __init__(self,n):
        self.n = n
    def __iter__(self):
        num = self.n
        count = 0
        while (count<num):
            yield count
            count += 1

for i in MyRange(10):
    print i
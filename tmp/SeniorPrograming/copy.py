#coding=utf-8
"""
shallow copy (copy())操作创建一个新的容器，其包含的引用指向原对象中的对象。
deep copy (deepcopy())创建的对象包含的引用指向复制出来的新对象。
"""

import copy

a = [1,2,3]
b = a

#normal
print id(a) == id(b)        #true
print id(a[0]) == id(b[0])  #true

#shallow copy
c = copy.copy(a)
print id(c) == id(a)        #false
print id(c[0]) == id(a[0])  #true

#deep copy
d = copy.deepcopy(a)
print id(d) == id(a)        #false
print id(d[0]) == id(a[0])  #flase


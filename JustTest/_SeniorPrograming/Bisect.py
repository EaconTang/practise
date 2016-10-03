# coding=utf-8

'''
bisect模块能够提供保持list元素序列的支持。
它使用了二分法完成大部分的工作。
它在向一个list插入元素的同时维持list是有序的。
'''

import bisect

alist = [1, 2, 13, 14, 15, 41, 45, 46, 50, 250, 1500]

bisect.insort_right(alist, 10)
bisect.insort_left(alist, 11)

print alist

print len(alist)

# 返回应该插入的位置（但不插入）
print bisect.bisect(alist, 150)

#coding=utf-8
'''
eque是一种由队列结构扩展而来的双端队列(double-ended queue)，队列元素能够在队列两端添加或删除。
因此它还被称为头尾连接列表(head-tail linked list)，尽管叫这个名字的还有另一个特殊的数据结构实现。

Deque支持线程安全的，经过优化的append和pop操作，在队列两端的相关操作都能够达到近乎O(1)的时间复杂度。
虽然list也支持类似的操作，但是它是对定长列表的操作表现很不错，而
当遇到pop(0)和insert(0, v)这样既改变了列表的长度又改变其元素位置的操作时，其复杂度就变为O(n)了。
'''

import time
from collections import deque



# A sample to compare the deque&list's time
num = 1000

def append(list_deque):
    for i in range(num):
        list_deque.append(i)

def appendleft(list_deque):
    if isinstance(list_deque,list):
        for i in range(num):
            list_deque.insert(0,i)
    else:
        for i in range(num):
            list_deque.appendleft(i)

def pop(list_deque):
    for i in range(num):
        list_deque.pop()

def popleft(list_deque):
    if isinstance(list_deque,list):
        for i in range(num):
            list_deque.pop(0)
    else:
        for i in range(num):
            list_deque.popleft()

list_to_sort = deque([])

for container in [list,deque]:          #compare these two container's time
    for oper in [append,appendleft,pop,popleft]:        #functions to be compared
        alist = container(range(num))           #generate a list or deque
        start_time = time.time()
        oper(alist)
        #print "【",container.__name__,"】","【",oper.__name__,"】","Time spent:",time.time()-start_time

        #put into a list to sort by time
        list_to_sort.append((container.__name__,oper.__name__,time.time()-start_time))

print sorted(list_to_sort,key=lambda x:x[2])

#test rotate()
print list_to_sort
list_to_sort.rotate(2)
print list_to_sort
list_to_sort.rotate(-1)
print list_to_sort
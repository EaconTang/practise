#coding=utf-8
'''
heapq模块使用一个用堆实现的优先级队列。堆是一种简单的有序列表，并且置入了堆的相关规则。
堆是一种树形的数据结构，树上的子节点与父节点之间存在顺序关系。
二叉堆(binary heap)能够用一个经过组织的列表或数组结构来标识，在这种结构中，元素N的子节点的序号为2*N+1和2*N+2(下标始于0)。
简单来说，这个模块中的所有函数都假设序列是有序的，所以序列中的第一个元素(seq[0])是最小的，序列的其他部分
构成一个二叉树，并且seq[i]节点的子节点分别为seq[2*i+1]以及seq[2*i+2]。
当对序列进行修改时，相关函数总是确保子节点大于等于父节点。
'''

heap = []

for v in [10,20,50,40,30,456,56,45,6,5,75,6,56,4,56,2,345,65,7,6]:
    heapq.heappush(heap,v)
    print heap          #通过这里可看，总是确保最小数push到最前

#print heap

while heap:
    print heapq.heappop(heap)

portfolio = [
{'name': 'IBM', 'shares': 200, 'price': 91.1},
{'name': 'AAPL', 'shares': 50, 'price': 543.22},
{'name': 'FB', 'shares': 200, 'price': 21.09},
{'name': 'HPQ', 'shares': 45, 'price': 31.75},
{'name': 'YHOO', 'shares': 45, 'price': 16.35},
{'name': 'ACME', 'shares': 75, 'price': 115.65}
]

#nsmallest() nlargest()两个函数
#利用key值来排序
cheap = heapq.nsmallest(2,portfolio,key=lambda x:(x['shares'],x['price']))
expensive = heapq.nlargest(2,portfolio,key=lambda x:x['price'])

print cheap
print expensive
# coding=utf-8
import heapq


class PriorityQueue(object):
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        # 先根据优先级排序，再用全局index来对优先级相同的项排序
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


if __name__ == '__main__':
    q = PriorityQueue()
    q.push('a', 1)
    q.push('b', 6)
    q.push('c', 3)
    q.push('B', 6)
    print q.pop()
    print q.pop()
    print q.pop()
    print q.pop()

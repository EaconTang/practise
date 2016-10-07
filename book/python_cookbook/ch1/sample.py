# coding=utf-8
import os


def sum(items):
    # recursively implement sum() using *
    # head, *tail  = list(items)
    return head + sum(tail) if tail else head


# def sums(items: list) -> int:
#     returun sum(items)


def search(lines, pattern, history_length=5):
    """用deque实现保留有限的历史记录"""
    from collections import deque
    history_lines = deque(maxlen=history_length)
    for _ in lines:
        if pattern in _:
            yield _, history_lines
        history_lines.append(_)


def max_N(n, items):
    import heapq
    return heapq.nlargest(n, items)


def dict_sort(d):
    from operator import itemgetter
    # 用zip函数把字典反转键值转换为有序的元组列表
    print sorted(zip(d.values(), d.keys()))
    # 还是这样更直观
    print sorted(d.iteritems(), key=lambda x:x[1])


def reader(s, size):
    while True:
        data = s.recv(size)
        if data == b'':
            break
        # process data


def reader2(s, size):
    for data in iter(lambda: s.recv(size), b''):
        pass
        # process data


if __name__ == '__main__':
    dict_sort({1:1, 2:2, 3:3})




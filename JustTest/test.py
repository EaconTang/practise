# -*- coding: utf-8 -*-
class Node(object):
    def __init__(self, val):
        self.left = None
        self.right = None
        self.val = val

    @property
    def left(self):
        return self.left

    @property
    def right(self):
        return self.right

    @left.setter
    def left(self, val):
        self.left = val

    @right.setter
    def right(self, val):
        self.right = val


def print_tree(node):
    if node is not None and node.val is not None:
        print node.val + ' -> '
        if node.left is not None:
            print_tree(node.left)
        if node.right is not None:
            print_tree(node.right)
        print '\n'


def has_path(node, sum):
    if node.val is None or node.val > sum:
        return False
    elif node.val == sum and node.left is None and node.right is None:
        return True
    else:
        return has_path(node.left, sum - node.val) or has_path(node.right, sum - node.val)


if __name__ == '__main__':

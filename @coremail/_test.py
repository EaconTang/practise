# coding=utf-8
import datetime,time
import os
import unittest

class A:
    def __init__(self):
        print 'A init...'

class B(A):
    def __init__(self):
        super.__init__()
        print 'B init...'

    def test(self):
        print 'B test()...'

b = B()

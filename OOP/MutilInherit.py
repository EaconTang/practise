# coding=utf-8
import datetime, time
import os
import unittest
import ast
from multiprocessing import Pool
import threading
import binascii
import array
import re
import sys
import functools
import math


class Base(object):
    def __init__(self):
        self.base = 'hah'
        print 'Base'

    def x(self):
        raise NotImplementedError

    def y(self):
        raise NotImplementedError


class A(Base):
    def __init__(self):
        super(A, self).__init__()
        self.a = 1
        print 'A'

    def x(self):
        print 'x()'


class B(Base):
    def __init__(self):
        super(B, self).__init__()
        self.b = 2
        print 'B'




class D(Base):
    def __init__(self):
        super(D,self).__init__()
        self.d = 3
        print 'D'

    def y(self):
        print 'y()'


class C(A, B, D):
    def foo(self):
        print self.a
        print self.b
        print self.d


c = C()
print dir(c)
c.foo()
c.x()
c.y()
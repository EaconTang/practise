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

def do_dict(var):
    assert isinstance(var, dict)
    _var = {
        '1': 1,
        'a': 'a'
    }
    # var.update(_var)
    _var.update(var)
    print _var

d = {'b':'b'}
do_dict(d)
print d

print id(d)
D = d
print id(D)

class T(object):
    def __init__(self, d):
        self.d = d
        print id(self.d)

    def udict(self):
        _d = {'a':'a'}
        self.d.update(_d)

t = T(d)
t.udict()
print d
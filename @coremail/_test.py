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
import ConfigParser
from optparse import OptionParser
from contextlib import nested
import copy

def f_gen(filename):
    with open(filename) as f:
        for line in f:
            yield line
#
# def f_gens():
#     open_files = "open('temp'), open('test')"
#     with nested(eval(open_files)) as fs:
#         for open_file in fs:
#             for line in open_file:
#                 yield line



def gs(filenames):
    def _gens(filenames):
        # return a generator that gens generator(f_gen)
        for filename in filenames:
            yield f_gen(filename)

    gs = _gens(filenames)
    for g in gs:
        for i in g:
            yield i

a = {'a':1, 'b':2}
A = (i for i in xrange(10))
print id(A)
print id(list(A))
print id(len(list(A)))

la = list(A)
print id(la)


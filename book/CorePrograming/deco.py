# coding=utf-8
import time as t


def deco(func):
    def wrapfun():
        print 'Currrent time:', t.ctime(), '; Function name:', func.__name__
        return func()

    return wrapfun()


@deco
def foo():
    print 'haha'


foo()
t.sleep(3)

for i in range(10):
    foo()
    t.sleep(i)

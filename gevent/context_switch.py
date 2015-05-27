#coding:utf-8
'''
并发的核心思想在于，大的任务可以分解成一系列的子任务，后者可以被调度成 同时执行或异步执行，
而不是一次一个地或者同步地执行。两个子任务之间的 切换也就是上下文切换。

在gevent里面，上下文切换是通过yielding来完成的. 在下面的例子里，
我们有两个上下文，通过调用gevent.sleep(0)，它们各自yield向对方。
'''

import gevent
import time

def foo():
    print "foo() start...","at",time.ctime()
    gevent.sleep(1)
    print "foo() end...","at",time.ctime()

def bar():
    print "bar() start...","at",time.ctime()
    gevent.sleep(2)
    print "bar() end...","at",time.asctime()

gevent.joinall([gevent.spawn(bar),gevent.spawn(foo)])
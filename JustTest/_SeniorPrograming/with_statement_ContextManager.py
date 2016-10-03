# coding=utf-8
'''
with语句是对try…expect…finally语法的一种简化，是一种上下文的管理协议
with后面的语句被求值后，返回对象的__enter__()被调用，__enter__返回值赋值给as后面的变量
当with后面的代码块全部被执行完之后，将调用前面返回对象的__exit__()方法;
如果有异常出现，就传入__exit__()参数

'''


# 通过类方法管理上下文
class Sample:
    def __init__(self):
        print 'haha'

    def __enter__(self):
        print 'call __enter__....'
        return self

    def __exit__(self, exc_type, exc_val, exc_trace):
        print 'call __exit__...'
        print 'exc_type:', exc_type
        print 'exc_val:', exc_val
        print 'exc_trace', exc_trace

    # 制造异常给__exit__
    def exc(self):
        return 1 / 0

    def exc2(self):
        return open('a.txt')


def getSample():
    return Sample()


with Sample() as sample:
    print 'value(of sample) received from __enter__:', sample
    sample.exc()
    # sample.exc2()          #_exit__()只捕获了第一个异常？

# 另外还有通过装饰器的方法
'''
一个确保代码执行前加锁，执行后释放锁的模板：
@contextmanager
def locked(lock):
    lock.acquire()
    try:
        yield
    finally:
        lock.release()

with locked(myLock):
    pass
    # Code here executes with myLock held.  The lock is
    # guaranteed to be released when the block is left (even
    # if via return or by an uncaught exception).
'''

# coding=utf-8
'''
常见的装饰器模式：
    1. 参数检查
    2. 缓存
    3. 代理
    4. 上下文提供者
'''
import pickle, hashlib

#########缓存模式##########
cache = {}


def compute_hashkey(func, arg, kwargs):
    p = pickle.dumps((func.func_name, arg, kwargs))
    return hashlib.sha1(p).hexdigest()


def memoize(duration=10):
    # could do something with duration
    def _memoize(function):
        def __memoize(*args, **kwargs):
            hashkey = compute_hashkey(function, args, kwargs)
            if hashkey in cache:
                print 'return from cache...'
                return cache[hashkey]
            value = function(*args, **kwargs)
            cache[hashkey] = value
            print 'new this value to cache: ', cache
            return value

        return __memoize

    return _memoize


@memoize()
def add(a, b):
    return a + b

if __name__ == '__main__':
    print add(1, 2)
    print add(2, 3)
    print add(1, 4)
    print add(4, 1)
    print add(1, 2)
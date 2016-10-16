from functools import wraps


def call_times(func):
    d = dict(ncalls=0)

    @wraps(func)
    def wrapper(*args, **kwargs):
        # use mutable type in py2
        # use nonlocal in py3
        d['ncalls'] += 1
        return func(*args, **kwargs)
    wrapper.ncalls = lambda: d['ncalls']
    return wrapper


@call_times
def add(a, b):
    print a + b


if __name__ == '__main__':
    add(1, 2)
    add(2, 2)
    print add.ncalls()
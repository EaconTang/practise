from functools import wraps
from inspect import *


def typecheck(*ty_args, **ty_kwargs):
    def decorate(func):
        if not __debug__:
            return func

        # print getargspec(func)
        _args, varargs, varkw, defaults = getargspec(func)
        expect_arg_type = dict(zip(_args, ty_args))
        expect_arg_type.update(**ty_kwargs)

        # print expect_arg_type

        @wraps(func)
        def wrapper(*args, **kwargs):
            callargs = getcallargs(func, *args, **kwargs)
            for key in callargs.keys():
                if not isinstance(callargs[key], expect_arg_type.get(key, object)):
                    raise TypeError('Arg {} expect {}, got {}'.format(key, expect_arg_type[key], type(callargs[key])))
            return func(*args, **kwargs)

        return wrapper

    return decorate


@typecheck(x=int, y=str)
def foo(x, y, z=0, a=1, b=2, *args, **kwargs):
    print str(y) * int(x)


if __name__ == '__main__':
    foo(2, 'bar')

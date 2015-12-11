# coding=utf-8

def trace():
    def _trace(f):
        def __trace(*args,**kwargs):
            print "calling function: {0} \n\twith args {1}, {2}".format(f.func_name,args,kwargs)
            return f(*args,**kwargs)
        return __trace
    return _trace

@trace()
def echo(text,kv={'a':1}):
    print text
    print kv


if __name__ == '__main__':
    echo('haha')
    echo(text='hiahiahia',kv={'b':2})
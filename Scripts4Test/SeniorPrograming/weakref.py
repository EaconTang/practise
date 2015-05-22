import gc


class Foo(object):
    """
    Scripts4Test strong reference
    """
    def __init__(self):
        self.obj = None
        print 'created'

    def __del__(self):
        print 'destroyed'

    def show(self):
        print self.obj

    def store(self, obj):
        self.obj = obj

a = Foo() # created
b = a
del a
print 'hahha'
del b # destroyed


#Scripts4Test wearkref.ref
a = Foo()
b = weakref.ref(a)
del a
print 'haha'
del b

#Scripts4Test weakref.proxy
a = Foo()
b = weakref.proxy(a)
del a
print 'haha'
del b
#print b.show()     #use "proxy" would raise except

class MyObject(object):
    def my_method(self):
        print 'my_method was called!'

obj = MyObject()
r = weakref.ref(obj)

gc.collect()
assert r() is obj #r() allows you to access the object referenced: it's there.

obj = 1 #Let's change what obj references to
gc.collect()
assert r() is None #There is no object left: it was gc'ed.
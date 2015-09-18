'''
4 ways to implement singleton pattern in python
'''

#----------------1---------------------
class Singleton01(object):
    '''implement a __new__ method && bind the instance to a class variable'''
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            orig = super(Singleton01,cls)
            cls._instance = orig.__new__(cls,*args,**kwargs)

        return cls._instance

class MyClass01(Singleton01):
    a = ''

#----------------2---------------------
class Singleton02(object):
    '''share a public class atttibute(dict)
       so each instance has different id but the same state'''
    _state = {}
    def __new__(cls, *args, **kwargs):
        obj = super(Singleton02,cls).__new__(cls,*args,**kwargs)
        obj.__dict__ = cls._state
        return obj

class MyClass02(Singleton02):
    a = ''

#----------------3---------------------
class Singleton03(type):        #it's a 'type'
    '''metaclass'''
    def __init__(cls, name, bases, dict):
        super(Singleton03, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton03, cls).__call__(*args, **kwargs)
        return cls._instance

class MyClass03(object):
    __metaclass__ = Singleton03

#----------------4---------------------
def Singleton04(cls,*args,**kwargs):
    '''decorator(recommend,more pythonic and elegant)'''
    instances = {}      # save all decorated class's instance(only one)
    def _Singleton():
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return _Singleton

@Singleton04
class MyClass04(object):
    a = ''
    def __init__(self):
        pass



if __name__ == '__main__':
    s1 = MyClass01()
    s2 = MyClass01()
    print id(s1)
    print id(s2)
    s2.a = 'test'
    print s1.a
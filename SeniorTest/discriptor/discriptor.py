'''
test data discriptor
'''

# By override class method
class DiscriptorA:
    def __init__(self,x):
        self.x = x

    def __get__(self, instance, owner):
        print 'get haha...'
        return self.x

    def __set__(self, instance, value):
        print 'set haha....'
        assert isinstance(value,int),'x must be a integer'
        self.x = value

    def __delete__(self, instance):
        print 'deleting!!!'
        del self.x


# By property class
class DiscriptorB:
    def __init__(self):
        self.x = 0

    def fget(self):
        print 'getting...'
        return self.x

    def fset(self,value):
        print 'setting...'
        assert isinstance(value,int)
        self.x = value

    def fdel(self):
        print 'deleting...'
        del self.x

    x = property(fget=,fset=,fdel=,doc='This is the property.')


# By property modifiers
class DiscriptorC:
    def __init__(self):
        self.x = 0

    @property
    def x(self):
        print 'get!'
        return self.x

    @x.setter
    def x(self,value):
        print 'set!'
        assert isinstance(value,int)
        self.x = value

    @x.deleter
    def x(self):
        print 'delete!'
        del self.x


# Dinamically auto-generate the discriptor
class DiscriptorD:
    def add_property(self,property_name):
        getter = lambda self: self.fget(property_name)
        setter = lambda self,v: self.fset(v,property_name)
        delter = lambda self: self.fdel(property_name)
        value = property(getter,setter,delter,doc='This is auto-generate!')
        setattr(self.__class__,property_name,value)

    def fget(self,name=''):
        print 'auto get {0}...'.format(name)
        return getattr(self,name)

    def fset(self,value,name):
        print 'auto set {0}...'.format(name)
        return setattr(self,name,value)

    def fdel(self,name):
        print 'auto del {0}...'.format(name)
        delattr(self,name)



class TestDiscri:
    d1 = DiscriptorA(1)
    d2 = DiscriptorB()
    d3 = DiscriptorC()


if __name__ == '__main__':

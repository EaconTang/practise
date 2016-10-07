from collections import namedtuple

Person = namedtuple('person', ['name', 'age', 'sex'])
p1 = Person('tyk', 23, 'male')
p2 = Person(name='eacon', sex='male', age=24)
print p1
print p2

print id(p1)
p1 = p1._replace(age=24)
print id(p1)

from operator import itemgetter
print tuple(p1)

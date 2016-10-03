def myGen():
    yield 1
    yield 2
    yield "last one!"


gen1 = myGen()

print gen1.next()

print gen1.next()
print gen1.next()

from random import randint


def ranGen(aList):
    while len(aList) > 0:
        yield aList.pop(randint(0, len(aList)))


for each in ranGen([1, 2, 3, 4, 5]):
    print each

print('haha')

aRangen = ranGen([6, 7, 8, 9, 10])
print aRangen.next()
print aRangen.next()
print aRangen.next()
print aRangen.next()
print aRangen.next()

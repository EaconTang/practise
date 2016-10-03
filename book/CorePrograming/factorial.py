__author__ = 'eacon'


def fact(n):
    if n == 1 or n == 0:
        return 1
    else:
        return (n ** 2) * fact(n - 2)


print fact(5)

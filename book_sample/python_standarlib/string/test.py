import string

trans = string.maketrans('tyingk', 'yktang')
s = "i am tyingk"

print s.translate(trans)

t = string.Template(
    "$name is ${age}!"
)
print t.safe_substitute(name='tyk', age=18)


class MyTemplate(string.Template):
    delimiter = '%'
    idpattern = '_[a-z]+'


f = open('temp.txt')
s = f.readlines()
l1 = s[0].strip().split(',')
l2 = s[1].strip().split(',')

print 'this week,the heighest temperature is :', max(l1), 'at day:', l1.index(max(l1)) + 1
print 'this week,the heighest temperature is :', min(l2), 'at day:', l2.index(min(l2)) + 1

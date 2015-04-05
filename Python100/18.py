n = int(raw_input('input the times:'))
a = int(raw_input('input the number:'))

s = 0
l = []
sum = 0

for i in range(n):
	s = s + a
	l.append(s)
	a = a*10

sum1 = reduce(lambda x,y :x+y,l)
print sum1

for i in l:
	sum = sum + i

print sum


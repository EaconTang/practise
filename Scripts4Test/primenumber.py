import math

a = int(raw_input('input a number:'))
n = int(math.sqrt(a))

if a >= 4:
	for i in range(2,n+1):
		if a%i == 0:
			print a,'is a prime!','cause',a,'%',i,'= 0 !'
			break
		if i == n:
			print a,'is not a prime!'
elif 0<a<4:
	print a,'is a prime obviously!'

else:
	print a,'is not a prime!'
			
		
		

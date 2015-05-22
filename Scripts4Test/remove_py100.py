import os
import string

path = os.getcwd()
List = os.listdir(path)
os.system('mkdir mvto')

#str = '.py'
str1 = 'JCP00'
for i in range(1,10):
	fname = str(i) + '.py'
	if fname in List:
		pass
	else:
		mvname = str1 + str(i) + '.py'
		os.system('mv %s mvto'%mvname)

str2 = 'JCP0'
for i in range(10,100):
	fname = str(i) + '.py'
	if fname in List:
		pass
	else:
		mvname = str2 + str(i) + '.py'
		os.system('mv %s mvto'%mvname)

print os.listdir(path)
os.system('rm -rf mvto')

	
	

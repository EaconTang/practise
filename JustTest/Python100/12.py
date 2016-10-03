from math import sqrt

count = 0  # 计算多少个素数
leap = 1        ＃判断是否break过，即是否非素数
for i in range(101, 201):
    a = int(sqrt(i))
    for d in range(2, a + 1):
        if (i % d == 0):
            leap = 0
            break        ＃非素数，可以跳出内循环
    if (leap == 1):
        print i,
        count += 1
    leap = 1
print '\nTotal prime:', count

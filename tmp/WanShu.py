#coding:utf8

m=1000
for a in range(2,m+1):
    s=a
    L1=[]
    for i in range(1,a):
        if a%i==0:
            s-=i
            L1.append(i)
    if s==0:
        print "WanShu：%d，YinZi："%a,
        for j in range(0,len(L1)):
            print "%d"%L1[j],
        print "\n" 

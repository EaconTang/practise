def han(n,a,b,m):
    if n == 1:
        print a,'->',b
    else:
        han(n-1,a,m,b)
        print a,'->',b
        han(n-1,m,b,a)

han(10,'A','B','M')
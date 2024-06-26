def a(b):
    if b==3:
        c=[1,2,3]
    if b==0:
        return
    print(c)
    c=c[:-1]
    return a(b-1)

a(3)
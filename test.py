


a=[0,0]
b=[0,0]
while b!=a or a.count(0)==len(a):
    if b!=a:
        b[-1]+=1
    else:
        a[-1]+=1
        
    for i in range(-1,-len(b),-1):
        
        if b[i]>a[i]:
            b[i-1]+=1
            b[i]=0
        
        print(b)
        
                 
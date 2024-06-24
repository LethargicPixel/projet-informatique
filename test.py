a=[2,2]
b=[0,0]
b[-1]-=1
c=True
while b!=a and c:        
    
    
    if b==a and a.count(0)==len(a):        
        c=False    
    else:
        b[-1]+=1
    
    
    for i in range(-1,-len(b),-1):
        
        if b[i]>a[i]:
            b[i-1]+=1
            b[i]=0
    print(b)
a=1
b=1
c=0

n=int(input())
for i in range(n):
    c=a+b
    print(c)
    a=b
    b=c

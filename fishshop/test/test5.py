# 1.求出1-100之间的和
a=0
for i in range(101):
    a+=i
print(a)
#方法2
print(sum(range(101)))

#2.冒泡排序
b=[1,3,2,5,7,4]
j=len(b)
for i in range(j):
    for k in range(i):
        if b[i-k-1]>b[i-k]:
            b[i-k-1],b[i-k]=b[i-k],b[i-k-1]
for i in range(len(b)):
    print(b[i])
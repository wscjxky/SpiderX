import os

lst = []
str = input("请输入数值，用空格隔开:")
lst1 = str.split(" ")
i = 0
while i < len(lst1):
    lst.append(float(lst1[i]))
    i += 1
def sum(list):
    print(list)
    re=0
    for i in range(1,6):
        re+=(list[i+5]-list[i])/5
    re /= 5.0
    return  re

print (sum(lst))
os.system("pause")
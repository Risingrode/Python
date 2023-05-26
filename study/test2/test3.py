import math
import random
import unicodedata
# 引入日历模块
import calendar
# 用于获取昨天日期
import datetime
# 实现秒表
import time
# 引入url
import re

'''笛卡尔积
import itertools

class cartesian(object):
    count=0
    def __init__(self):
        self._data_list=[]

    def add_data(self,data=[]): #添加生成笛卡尔积的数据列表
        self._data_list.append(data)

    def build(self): #计算笛卡尔积
        for item in itertools.product(*self._data_list):
            print(item,end=" ")
            self.count+=1
            if self.count%16==0:
                print()

if __name__=="__main__":
    car=cartesian()
    car.add_data([1,2,3,4])
    car.add_data([5,6,7,8])
    car.add_data([9,10,11,12])
    car.build()
'''

# a = int(input("请输入圆半径："))


# print("圆面积是：{0:.2f}".format(math.pi * a * a))
# print(random.randint(0,9))
# print('%0.1f 摄氏温度转为华氏温度为 %0.1f ' % (celsius, fahrenheit))

# print('a是%0.2f,b是%d' % (a, b))

# lower=int(input('最小值是：'))
# upper=int(input('最大值是：'))
# for x in range(lower,upper+1):
#     sum=0
#     n=len(str(x))
#     temp=x
#     while temp>0:
#         d=temp%10
#         sum+=d**n
#         temp//=10
#     if x==sum:
#         print(x,end=" ")

#   bin()  oct() hex()
#   asc码与字符转化 ord()     cha()
#   range（）函数是左闭右开
#    print(a, '/', b, '=', chu(a, b))


#   print(calendar.month(y,x))

# with open('测试.txt','w') as wile:
#    wile.write('厉害！')

# 获取今天日期
#   print(datetime.date.today())
#   print(datetime.date.today()-datetime.timedelta(days=1))


#   li.pop()  # pop 会做两件事: 删除 list 的最后一个元素, 然后返回删除元素的值
# append    index   insert  remove  pop     extend

# print(','.join(list))
# s=','.join(list)
# print(s.split(','))

# time.sleep(1.1)   秒
# round(end-start,2)    时间精确到后面2位
# a,b=b,a   可以达到交换的作用

#  li_copy = li1[:] 复制列表
#  ord() 把给定的字符转化为ascII码

a = []
for x in range(1, 10):
    a.append(random.randint(1, 100))


# 插排
def insertSort(arr):
    for i in range(1, len(arr)):
        temp = arr[i]
        j = i - 1
        while j >= 0 and temp < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = temp


# 希尔排序
def shellSort(arr):
    gap = int(len(arr) / 2)
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and temp < arr[j-gap]:
                arr[j] = arr[j-gap]
                j -= gap
            arr[j] = temp
        gap =int(gap/2)


def countSort(arr):
    ae=[0 for x in range(256)]
    b = []
    for i in arr:
        ae[i]+=1
    x=0
    for i in ae:
        temp=i
        while temp:
            b.append(x)
            temp-=1
        x+=1
    return b





print(countSort(a))

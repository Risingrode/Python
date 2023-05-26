import random


# 计算x^3-x^2 在[a,b]之间的面积

def Algorithm(n):
    result = 0.0
    for i in range(n):
        x = random.uniform(1, 2)
        y = random.uniform(0, 4)
        if (x * x * x - x * x) >= y:  # 这里是关键，也是精髓
            result += 1
    res = (result / float(n)) * 4.0
    print('面积是：%f' % res)


a = input('请输入模拟次数：')
Algorithm(int(a))

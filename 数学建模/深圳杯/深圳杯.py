import math  # 导⼊模块
import random  # 导⼊模块
import pandas as pd  # 导⼊模块 YouCans, XUPT
import numpy as np  # 导⼊模块 numpy，并简写成 np
import matplotlib.pyplot as plt
from datetime import datetime


# ⼦程序：定义优化问题的⽬标函数
def cal_Energy(X, nVar, mk):  # m(k)：惩罚因⼦，随迭代次数 k 逐渐增⼤

    p1 = (max(0, 6 * X[0] + 5 * X[1] - 60)) ** 2
    p2 = (max(0, 10 * X[0] + 20 * X[1] - 150)) ** 2
    fx = -(10 * X[0] + 9 * X[1])
    return fx + mk * (p1 + p2)


# ⼦程序：模拟退⽕算法的参数设置
def ParameterSetting():
    cName = "funcOpt"  # 定义问题名称 YouCans, XUPT
    nVar = 2  # 给定⾃变量数量，y=f(x1,..xn)
    xMin = [0, 0]  # 给定搜索空间的下限，x1_min,..xn_min
    xMax = [8, 8]  # 给定搜索空间的上限，x1_max,..xn_max
    tInitial = 100.0
    tFinal = 1
    alfa = 0.98
    meanMarkov = 100  # Markov链长度，也即内循环运⾏次数
    scale = 0.5  # 定义搜索步长，可以设为固定值或逐渐缩⼩
    return cName, nVar, xMin, xMax, tInitial, tFinal, alfa, meanMarkov, scale


# 模拟退⽕算法
def OptimizationSSA(nVar, xMin, xMax, tInitial, tFinal, alfa, meanMarkov, scale):

    # ====== 初始化随机数发⽣器 ======
    randseed = random.randint(1, 100)
    random.seed(randseed)  # 随机数发⽣器设置种⼦，也可以设为指定整数
    # ====== 随机产⽣优化问题的初始解 ======
    xInitial = np.zeros((nVar))  # 初始化，创建数组
    for v in range(nVar):
        # xInitial[v] = random.uniform(xMin[v], xMax[v]) # 产⽣ [xMin, xMax] 范围的随机实数
        xInitial[v] = random.randint(xMin[v], xMax[v])  # 产⽣ [xMin, xMax] 范围的随机整数
    # 调⽤⼦函数 cal_Energy 计算当前解的⽬标函数值
    fxInitial = cal_Energy(xInitial, nVar, 1)  # m(k)：惩罚因⼦，初值为 1
    # ====== 模拟退⽕算法初始化 ======
    xNew = np.zeros((nVar))  # 初始化，创建数组
    xNow = np.zeros((nVar))  # 初始化，创建数组
    xBest = np.zeros((nVar))  # 初始化，创建数组
    xNow[:] = xInitial[:]  # 初始化当前解，将初始解置为当前解
    xBest[:] = xInitial[:]  # 初始化最优解，将当前解置为最优解
    fxNow = fxInitial  # 将初始解的⽬标函数置为当前值
    fxBest = fxInitial  # 将当前解的⽬标函数置为最优值
    print('x_Initial:{:.6f},{:.6f},\tf(x_Initial):{:.6f}'.format(xInitial[0], xInitial[1], fxInitial))
    recordIter = []  # 初始化，外循环次数
    recordFxNow = []  # 初始化，当前解的⽬标函数值
    recordFxBest = []  # 初始化，最佳解的⽬标函数值
    recordPBad = []  # 初始化，劣质解的接受概率
    kIter = 0  # 外循环迭代次数
    totalMar = 0  # 总计 Markov 链长度
    totalImprove = 0  # fxBest 改善次数
    nMarkov = meanMarkov  # 固定长度 Markov链
    # ====== 开始模拟退⽕优化 ======
    # 外循环
    tNow = tInitial  # 初始化当前温度(current temperature)
    while tNow >= tFinal:  # 外循环
        kBetter = 0  # 获得优质解的次数
        kBadAccept = 0  # 接受劣质解的次数
        kBadRefuse = 0  # 拒绝劣质解的次数
        # ---内循环，循环次数为Markov链长度
    for k in range(nMarkov):  # 内循环，循环次数为Markov链长度
        totalMar += 1  # 总 Markov链长度计数器
    # ---产⽣新解
    # 产⽣新解：通过在当前解附近随机扰动⽽产⽣新解，新解必须在 [min,max] 范围内
    # ⽅案 1：只对 n元变量中的⼀个进⾏扰动，其它 n-1个变量保持不变
    xNew[:] = xNow[:]
    v = random.randint(0, nVar - 1)  # 产⽣ [0,nVar-1]之间的随机数
    xNew[v] = round(xNow[v] + scale * (xMax[v] - xMin[v]) * random.normalvariate(0, 1))
    # 满⾜决策变量为整数，采⽤最简单的⽅案：产⽣的新解按照四舍五⼊取整
    xNew[v] = max(min(xNew[v], xMax[v]), xMin[v])  # 保证新解在 [min,max] 范围内
    # ---计算⽬标函数和能量差
    # 调⽤⼦函数 cal_Energy 计算新解的⽬标函数值
    fxNew = cal_Energy(xNew, nVar, kIter)
    deltaE = fxNew - fxNow
    # ---按 Metropolis 准则接受新解
    # 接受判别：按照 Metropolis 准则决定是否接受新解
    if fxNew < fxNow:  # 更优解：如果新解的⽬标函数好于当前解，则接受新解
        accept = True
        kBetter += 1
    else:  # 容忍解：如果新解的⽬标函数⽐当前解差，则以⼀定概率接受新解
        pAccept = math.exp(-deltaE / tNow)  # 计算容忍解的状态迁移概率
    if pAccept > random.random():
        accept = True  # 接受劣质解
        kBadAccept += 1
    else:
        accept = False  # 拒绝劣质解
        kBadRefuse += 1
    # 保存新解
    if accept == True:  # 如果接受新解，则将新解保存为当前解
        xNow[:] = xNew[:]
        fxNow = fxNew
    if fxNew < fxBest:  # 如果新解的⽬标函数好于最优解，则将新解保存为最优解
        fxBest = fxNew
    xBest[:] = xNew[:]
    totalImprove += 1
    scale = scale * 0.99  # 可变搜索步长，逐步减⼩搜索范围，提⾼搜索精度
    # ---内循环结束后的数据整理
    #
    pBadAccept = kBadAccept / (kBadAccept + kBadRefuse)  # 劣质解的接受概率
    recordIter.append(kIter)  # 当前外循环次数
    recordFxNow.append(round(fxNow, 4))  # 当前解的⽬标函数值
    recordFxBest.append(round(fxBest, 4))  # 最佳解的⽬标函数值
    recordPBad.append(round(pBadAccept, 4))  # 最佳解的⽬标函数值

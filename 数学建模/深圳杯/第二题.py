import numpy as np
from itertools import product

class Lorry:
    def __init__(self, station1, station2):
        # station1: P->D 换电站位置， station2：D->P 换电站位置
        self.bet = 100  # 当前电池电量
        self.p = 20 - station2  # 当前位置
        self.t = 0  # 当前时间
        self.station1 = station1
        self.station2 = station2
        self.n_charge = 0  # 充电次数
        self.n_mission = 0  # 运货次数

    def __str__(self):
        return "Lorry is at position {:.1f}, charged {:d} times,\n complete mission {:d} times in {:.1f} minutes".format(
            self.p, self.n_charge, self.n_mission, self.t)

    def move(self, dt):
        # 0(P)___10(D)___20(P')
        # dt时间后的演化结果
        if 0 <= self.p < 10 or np.isclose(self.p, 0):
            # P->D
            self.bet -= 1 / 2 * dt  # 电池消耗
        elif 10 <= self.p < 20 or np.isclose(self.p, 10):
            # D->P
            self.bet -= 1 / 3 * dt  # 电池消耗
        if self.bet < 0 or np.isclose(self.bet, 0):
            raise Exception("Lorry is out of battery")
        self.t = self.t + dt  # 时间变化
        self.p = (self.p + dt * 1) % 20  # 位置变化
        if np.isclose(self.p, 0):
            # 装卸货时间
            self.t += 1
        elif np.isclose(self.p, 10):
            self.t += 1
            self.n_mission += 1
        self.recharge()

    def recharge(self):
        # 逐渐降低阈值，测试是否存在可行解
        if np.isclose(self.p, self.station1) and 10 <= self.bet <= 12.6:
            # 满载到达换电站
            self.bet = 100
            self.t += 2
            self.n_charge += 1
        elif np.isclose(self.p, 20 - self.station2) and 10 <= self.bet <= 12.6:
            # 空载到达换电站
            self.bet = 100
            self.t += 2 / 3  # 只考虑换电为2, 考虑换电为2/3
            self.n_charge += 1


lorry = Lorry(7.0, 2.0)
print("选址位于(7.0, 2.0)")
while lorry.t < (1000 * 60 - 0.1):
    lorry.move(dt=0.1)
print(lorry)

# lorry = Lorry(5.0, 5.0)
# print("选址位于(5.0, 5.0)")
# while lorry.t < (1000 * 60 - 0.1):
#     lorry.move(dt=0.1)
# print(lorry)
#
# lorry = Lorry(3.0, 8.0)
# print("选址位于(3.0, 8.0)")
# while lorry.t < (1000 * 60 - 0.1):
#     lorry.move(dt=0.1)
# print(lorry)

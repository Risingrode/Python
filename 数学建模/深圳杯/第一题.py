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

    def __str__(self):
        return "Lorry is at position {}, with battery {}, at time {}".format(self.p, self.bet, self.t)

    def move(self, dt):  # dt是当前电量
        if 0 <= self.p < 10:  # 满载状态
            self.bet -= 1 / 2 * dt  # 电池消耗
        elif 10 <= self.p < 20:  # 空载状态
            self.bet -= 1 / 3 * dt  # 电池消耗
        if self.bet <= 0:
            raise Exception("Lorry is out of battery")
        self.t = self.t + dt  # 时间变化
        self.p = (self.p + dt * 1) % 20  # 位置变化
        if np.isclose(self.p, 10) or np.isclose(self.p, 0):
            # 装卸货时间
            self.t += 1
        self.recharge()

    def recharge(self):
        if (np.isclose(self.p, self.station1) or np.isclose(self.p, 20 - self.station2)) and 10 <= self.bet <= 12.6:
            self.bet = 100
            self.t += 2  # 换一个电池20s
            self.n_charge += 1


if __name__ == '__main__':
    count = 0
    res = 0
    for sta1 in np.arange(0.1, 10, 0.1):  # 返回一个有终点和起点的固定步长的排列
        sta2 = sta1
        lorry = Lorry(sta1, sta2)
        try:
            for T in range(1000 * 60 * 10):  # 1000个小时中有多少个10s
                lorry.move(dt=0.1)
                print('({:.1f}, {:.1f}) worked with charge {:d} times'.format(sta1, sta2, lorry.n_charge))
            if (count < lorry.n_charge):
                res = sta1
                count = lorry.n_charge
        except Exception as e:
            print((sta1, sta2), e, end='\r')
    print('在{}位置的充电次数是{}'.format(res, count))
#4.9 km处   285次
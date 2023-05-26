import numpy as np


class Gomoku(object):
    def __init__(self, gsize=None, line=5) -> None:
        super().__init__()
        if gsize is None:
            self.size = 8
        else:
            self.size = gsize
        self.line = line
        self.grid = np.zeros([2, self.size, self.size], dtype=np.int)
        self.n_actions = self.size ** 2
        self.n_features = self.size ** 2 * 2

    def inside(self, xx, yy):
        return 0 <= xx < self.size and 0 <= yy < self.size

    def act_legal(self, action):
        xx = action[0]
        yy = action[1]
        if not self.inside(xx, yy):
            print('Out of Grid!')
        if self.grid[0, xx, yy] == 1:
            print('Self')
        elif self.grid[1, xx, yy] == -1:
            print('Rival')
        return 0 <= xx < self.size and 0 <= yy < self.size and self.grid[0, xx, yy] == 0 and self.grid[1, xx, yy] == 0

    def step(self, action):
        action = [action // self.size, action % self.size]
        if not self.act_legal(action):
            print("Illegal action!!!")
            exit(0)
        self.grid[0, action[0], action[1]] = 1
        dirs = [[0, 1], [1, 0], [1, 1], [1, -1]]
        for i in range(4):
            l1 = 1
            while True:
                xx = action[0] + dirs[i][0] * l1
                yy = action[1] + dirs[i][1] * l1
                if self.inside(xx, yy) and self.grid[0, xx, yy] == 1:
                    l1 += 1
                else:
                    break
            l2 = 1
            while True:
                xx = action[0] - dirs[i][0] * l2
                yy = action[1] - dirs[i][1] * l2
                if self.inside(xx, yy) and self.grid[0, xx, yy] == 1:
                    l2 += 1
                else:
                    break
            if l1 + l2 > self.line:
                self.turn()
                return self.get_state(), 1, True
        self.turn()
        return self.get_state(), 0, np.sum(self.grid ** 2) == self.size ** 2 * 2

    def reset(self):
        self.grid = np.zeros_like(self.grid)

    def turn(self):
        self.grid[[0, 1], :, :] = self.grid[[1, 0], :, :]

    def get_state(self):
        return np.array(self.grid).flatten()

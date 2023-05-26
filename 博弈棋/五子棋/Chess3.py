import pygame
import random

# 初始化pygame
pygame.init()
# 设置游戏窗口大小
WINDOW_SIZE = (500, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("五子棋")
# 设置游戏参数
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
ROW = 15
GAP = WINDOW_SIZE[0] // (ROW + 1)
RADIUS = GAP // 2 - 2


# 定义棋盘和棋子类
class Board:
    def __init__(self):
        self.rows = ROW
        self.grid = [[0] * self.rows for i in range(self.rows)]

    def draw(self):
        for i in range(self.rows):
            pygame.draw.line(screen, BLACK, (GAP, GAP * (i + 1)), (WINDOW_SIZE[0] - GAP, GAP * (i + 1)), 2)
            pygame.draw.line(screen, BLACK, (GAP * (i + 1), GAP), (GAP * (i + 1), WINDOW_SIZE[0] - GAP), 2)

    def move(self, x, y, player):
        self.grid[x][y] = player
        # 判断是否获胜
        if self.check_win(x, y, player):
            return True
        return False

    def check_win(self, x, y, player):
        # 水平方向
        count = 1
        i = x
        while i >= 1 and self.grid[i][y] == player:
            count += 1
            i -= 1
        i = x
        while i < self.rows - 1 and self.grid[i + 1][y] == player:
            count += 1
            i += 1
        if count >= 5:
            return True
        # 垂直方向
        count = 1
        i = y
        while i >= 1 and self.grid[x][i] == player:
            count += 1
            i -= 1
        i = y
        while i < self.rows - 1 and self.grid[x][i + 1] == player:
            count += 1
            i += 1
        if count >= 5:
            return True
        # 左上-右下方向
        count = 1
        i = x
        j = y
        while i >= 1 and j >= 1 and self.grid[i][j] == player:
            count += 1
            i -= 1
            j -= 1
        i = x
        j = y
        while i < self.rows - 1 and j < self.rows - 1 and self.grid[i + 1][j + 1] == player:
            count += 1
            i += 1
            j += 1
        if count >= 5:
            return True
        # 左下-右上方向
        count = 1
        i = x
        j = y
        while i >= 1 and j < self.rows - 1 and self.grid[i][j + 1] == player:
            count += 1
            i -= 1
            j += 1
        i = x
        j = y
        while i < self.rows - 1 and j >= 1 and self.grid[i + 1][j] == player:
            count += 1
            i += 1
            j -= 1
        if count >= 5:
            return True
        return False


class Piece:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player

    def draw(self):
        if self.player == 1:
            pygame.draw.circle(screen, BLACK, (self.x, self.y), RADIUS)
        else:
            pygame.draw.circle(screen, WHITE, (self.x, self.y), RADIUS)


# 定义游戏主循环
def main():
    board = Board()
    pieces = []
    player = 1
    turn = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if turn % 2 == 0 and player == 1:
                    x = event.pos[0]
                    y = event.pos[1]
                    i = x // GAP - 1
                    j = y // GAP - 1
                    if i < 0 or i > ROW - 1 or j < 0 or j > ROW - 1:
                        continue
                    if board.grid[i][j] != 0:
                        continue
                    piece = Piece((i + 1) * GAP, (j + 1) * GAP, player)
                    pieces.append(piece)
                    if board.move(i, j, player):
                        print("Player 1 wins!")
                        running = False
                    player = 2
                    turn += 1
                elif turn % 2 == 1 and player == 2:
                    # 使用蒙特卡洛算法生成落子位置
                    best_move = monte_carlo(board, player)
                    if board.move(best_move[0], best_move[1], player):
                        print("Player 2 wins!")
                        running = False
                    piece = Piece((best_move[0] + 1) * GAP, (best_move[1] + 1) * GAP, player)
                    pieces.append(piece)
                    player = 1
                    turn += 1
        screen.fill(GRAY)
        board.draw()
        for piece in pieces:
            piece.draw()
        pygame.display.flip()
    pygame.quit()


# 定义蒙特卡洛算法
def monte_carlo(board, player):
    # 创建可行落子位置列表
    valid_moves = []
    for i in range(board.rows):
        for j in range(board.rows):
            if board.grid[i][j] == 0:
                valid_moves.append((i, j))
    # 在可行落子位置中随机选择5个位置进行模拟
    simulations = []
    for move in random.sample(valid_moves, 5):
        simulation_board = Board()
        simulation_board.grid = [row[:] for row in board.grid]
        simulation_board.move(move[0], move[1], player)
        winner = simulate(simulation_board, 3 - player)
        simulations.append((move, winner))
    # 根据模拟结果选择最佳落子位置
    best_score = -1
    best_move = None
    for move, winner in simulations:
        if winner == player:
            return move
        score = simulations.count((move, player))
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


# 定义模拟函数
def simulate(board, player):
    # 创建可行落子位置列表
    valid_moves = []
    for i in range(board.rows):
        for j in range(board.rows):
            if board.grid[i][j] == 0:
                valid_moves.append((i, j))
    # 随机选择可行落子位置进行模拟
    while valid_moves:
        i, j = random.choice(valid_moves)
        board.move(i, j, player)
        if board.check_win(i, j, player):
            return player
        player = 3 - player
        valid_moves.remove((i, j))
    return 0


# 启动游戏主循环
if __name__ == "__main__":
    main()

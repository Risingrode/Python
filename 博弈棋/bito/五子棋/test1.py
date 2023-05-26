import pygame
import random
import math

# 游戏参数
WIDTH = 640
HEIGHT = 640
ROWS = 15
COLUMNS = 15
SIZE = 40
PADDING = 5
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
GRAYBLUE = (70, 130, 180)
RED = (255, 0, 0)
FPS = 60
# 创建棋盘
board = [[" " for j in range(COLUMNS)] for i in range(ROWS)]
# 初始化pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Five in a Row")
# 加载字体
font = pygame.font.SysFont("comicsansms", 32)


def draw_board():
    """
    绘制棋盘
    """
    # 绘制背景
    screen.fill(GRAYBLUE)
    # 绘制行和列
    for i in range(ROWS):
        for j in range(COLUMNS):
            pygame.draw.rect(screen, BLACK,
                             (i * SIZE + PADDING, j * SIZE + PADDING, SIZE - 2 * PADDING, SIZE - 2 * PADDING), 1)
    # 绘制星位
    for i in range(3, 12, 4):
        for j in range(3, 12, 4):
            pygame.draw.circle(screen, BLACK, (i * SIZE + PADDING, j * SIZE + PADDING), 5)
    # 绘制棋子
    for i in range(ROWS):
        for j in range(COLUMNS):
            if board[i][j] == "B":
                pygame.draw.circle(screen, BLACK, (i * SIZE + PADDING, j * SIZE + PADDING), SIZE // 2 - 2)
            elif board[i][j] == "W":
                pygame.draw.circle(screen, WHITE, (i * SIZE + PADDING, j * SIZE + PADDING), SIZE // 2 - 2)


def is_valid_move(row, column):
    """
    判断是否为合法落子
    """
    if row < 0 or row >= ROWS or column < 0 or column >= COLUMNS or board[row][column] != " ":
        return False
    return True


def get_winner():
    """
    判断胜者
    """
    for i in range(ROWS):
        for j in range(COLUMNS):
            if board[i][j] != " ":
                # 横向判断
                if j <= COLUMNS - 5 and board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == \
                        board[i][j + 4]:
                    return board[i][j]
                # 纵向判断
                if i <= ROWS - 5 and board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == \
                        board[i + 4][j]:
                    return board[i][j]
                # 左上到右下判断
                if i <= ROWS - 5 and j <= COLUMNS - 5 and board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == \
                        board[i + 3][j + 3] == board[i + 4][j + 4]:
                    return board[i][j]
                # 右上到左下判断
                if i >= 4 and j <= COLUMNS - 5 and board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == \
                        board[i - 3][j + 3] == board[i - 4][j + 4]:
                    return board[i][j]
    return None


def get_legal_moves():
    """
    获取所有合法落子位置
    """
    legal_moves = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if board[i][j] == " ":
                legal_moves.append((i, j))
    return legal_moves


def update_board(row, column, player):
    """
    更新棋盘状态
    """
    board[row][column] = player


def get_random_move():
    """
    获取随机落子位置
    """
    legal_moves = get_legal_moves()
    return random.choice(legal_moves)


def mc_simulation(row, column, player):
    """
    蒙特卡洛模拟
    """
    wins = 0
    simulations = 1000
    for i in range(simulations):
        # 在棋盘上随机落子
        temp_board = [row[:] for row in board]
        temp_board[row][column] = player
        current_player = "B" if player == "W" else "W"
        while True:
            legal_moves = get_legal_moves()
            if not legal_moves:
                break
            move_row, move_column = random.choice(legal_moves)
            temp_board[move_row][move_column] = current_player
            if get_winner() is not None:
                if get_winner() == player:
                    wins += 1
                break
            current_player = "B" if current_player == "W" else "W"
    return wins / simulations


def get_best_move(player):
    """
    获取最佳落子位置
    """
    legal_moves = get_legal_moves()
    if not legal_moves:
        return None
    best_move = legal_moves[0]
    best_score = -1
    for move in legal_moves:
        score = mc_simulation(move[0], move[1], player)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def main():
    """
    游戏主循环
    """
    current_player = "B"
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_player == "B":
                    column = math.floor(event.pos[0] / SIZE)
                    row = math.floor(event.pos[1] / SIZE)
                    if is_valid_move(row, column):
                        update_board(row, column, current_player)
                        if get_winner() is not None:
                            text = font.render("Black wins!", True, RED)
                            screen.blit(text,
                                        (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                            pygame.display.flip()
                            pygame.time.wait(3000)
                            game_over = True
                        current_player = "W"
                elif current_player == "W":
                    row, column = get_best_move("W")
                    update_board(row, column, current_player)
                    if get_winner() is not None:
                        text = font.render("White wins!", True, RED)
                        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                        pygame.display.flip()
                        pygame.time.wait(3000)
                        game_over = True
                    current_player = "B"
        draw_board()
        pygame.display.flip()
        # 帧率控制
        pygame.time.Clock().tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()

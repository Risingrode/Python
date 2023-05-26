
import pygame

# 初始化 Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)

# 定义棋盘格子大小
BLOCK_SIZE = 40

# 定义棋盘尺寸
BOARD_WIDTH = BLOCK_SIZE * 15
BOARD_HEIGHT = BLOCK_SIZE * 15

# 创建 Pygame 窗口
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
pygame.display.set_caption('五子棋')

# 填充背景色
screen.fill(GREY)

# 画横线
for i in range(15):
    start_pos = (BLOCK_SIZE, BLOCK_SIZE * (i + 1))
    end_pos = (BLOCK_SIZE * 15, BLOCK_SIZE * (i + 1))
    pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)

# 画竖线
for i in range(15):
    start_pos = (BLOCK_SIZE * (i + 1), BLOCK_SIZE)
    end_pos = (BLOCK_SIZE * (i + 1), BLOCK_SIZE * 15)
    pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)

# 刷新画面
pygame.display.flip()

# Pygame 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()







































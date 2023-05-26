import pygame

class GobangBoard:
    def __init__(self):
        self.width = 640 # 棋盘宽度
        self.height = 640 # 棋盘高度
        self.line_width = 2 # 棋盘线宽
        self.cell_size = 40 # 棋盘单元格大小
        self.line_num = self.width // self.cell_size # 棋盘线数
        self.grid_size = self.cell_size * (self.line_num - 1) # 棋盘格子大小
        self.margin = (self.width - self.grid_size) // 2 # 棋盘边距
        self.piece_size = 36 # 棋子大小

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Gobang")
        self.clock = pygame.time.Clock()

    def draw_board(self):
        self.screen.fill((249, 214, 91)) # 背景颜色

        # 绘制棋盘网格线
        for i in range(self.line_num):
            start_pos = (self.margin + i * self.cell_size, self.margin)
            end_pos = (self.margin + i * self.cell_size, self.margin + self.grid_size)
            pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos, self.line_width)
            start_pos = (self.margin, self.margin + i * self.cell_size)
            end_pos = (self.margin + self.grid_size, self.margin + i * self.cell_size)
            pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos, self.line_width)

        # 绘制天元和星位
        center_pos = (self.margin + (self.line_num - 1) // 2 * self.cell_size, self.margin + (self.line_num - 1) // 2 * self.cell_size)
        pygame.draw.circle(self.screen, (0, 0, 0), center_pos, 4, 0)
        star_pos = [(self.margin + 3 * self.cell_size, self.margin + 3 * self.cell_size),
                    (self.margin + (self.line_num - 4) * self.cell_size, self.margin + 3 * self.cell_size),
                    (self.margin + 3 * self.cell_size, self.margin + (self.line_num - 4) * self.cell_size),
                    (self.margin + (self.line_num - 4) * self.cell_size, self.margin + (self.line_num - 4) * self.cell_size),
                    (self.margin + (self.line_num - 1) // 2 * self.cell_size, self.margin + (self.line_num - 1) // 2 * self.cell_size)]
        for pos in star_pos:
            pygame.draw.circle(self.screen, (0, 0, 0), pos, 4, 0)

        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.draw_board()
            self.clock.tick(60)

if __name__ == '__main__':
    board = GobangBoard()
    board.run()

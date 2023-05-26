from enum import IntEnum
import pygame

# 版本名称
GAME_VERSION = 'V1.0'

REC_SIZE = 50
CHESS_RADIUS = REC_SIZE // 2 - 2
CHESS_LEN = 15
MAP_WIDTH = CHESS_LEN * REC_SIZE
MAP_HEIGHT = CHESS_LEN * REC_SIZE

INFO_WIDTH = 200
BUTTON_WIDTH = 140
BUTTON_HEIGHT = 50

SCREEN_WIDTH = MAP_WIDTH + INFO_WIDTH
SCREEN_HEIGHT = MAP_HEIGHT


class MAP_ENTRY_TYPE(IntEnum):
    MAP_EMPTY = 0,
    MAP_PLAYER_ONE = 1,
    MAP_PLAYER_TWO = 2,
    MAP_NONE = 3,  # out of map range


# 用于保存五子棋数据和提供五子棋函数
class Map():
    def __init__(self, width, height):
        self.width = width  # 棋盘的宽
        self.height = height  # 棋盘的高
        # 棋盘
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]
        self.steps = []  # 按照顺序保存已经下的棋子
    # 初始化棋盘
    def reset(self):
        for y in range(self.height):
            for x in range(self.width):
                self.map[y][x] = 0
        self.steps = []
    # 转换下一个人
    def reverseTurn(self, turn):
        if turn == MAP_ENTRY_TYPE.MAP_PLAYER_ONE:
            return MAP_ENTRY_TYPE.MAP_PLAYER_TWO
        else:
            return MAP_ENTRY_TYPE.MAP_PLAYER_ONE

    def getMapUnitRect(self, x, y):
        map_x = x * REC_SIZE
        map_y = y * REC_SIZE

        return (map_x, map_y, REC_SIZE, REC_SIZE)

    def MapPosToIndex(self, map_x, map_y):
        x = map_x // REC_SIZE
        y = map_y // REC_SIZE
        return (x, y)
    # 检测是否合法
    def isInMap(self, map_x, map_y):
        if (map_x <= 0 or map_x >= MAP_WIDTH or
                map_y <= 0 or map_y >= MAP_HEIGHT):
            return False
        return True
    # 检测当前位置是否可以下棋
    def isEmpty(self, x, y):
        return (self.map[y][x] == 0)

    # 把该坐标绘制到棋盘上，并且存储步法
    def click(self, x, y, type):
        self.map[y][x] = type.value
        self.steps.append((x, y))

    def drawChess(self, screen):
        player_one = (255, 251, 240)# 棋子1颜色
        player_two = (88, 87, 86)# 棋子2颜色
        player_color = [player_one, player_two]# 颜色数组
        # 从系统字体库创建一个font对象
        font = pygame.font.SysFont(None, REC_SIZE * 2 // 3)

        # 绘制每一步棋子
        for i in range(len(self.steps)):
            x, y = self.steps[i]
            # 数值标准化
            map_x, map_y, width, height = self.getMapUnitRect(x, y)
            pos, radius = (map_x + width // 2, map_y + height // 2), CHESS_RADIUS
            turn = self.map[y][x]
            if turn == 1:
                op_turn = 2
            else:
                op_turn = 1
            # 绘制棋子
            pygame.draw.circle(screen, player_color[turn - 1], pos, radius)
            # render()渲染文本
            msg_image = font.render(str(i), True, player_color[op_turn - 1], player_color[turn - 1])
            msg_image_rect = msg_image.get_rect() # 获取图片在画布上的位置
            msg_image_rect.center = pos
            # 图片 中心位置 贴棋子
            screen.blit(msg_image, msg_image_rect)

        if len(self.steps) > 0:
            last_pos = self.steps[-1]
            # 标准化坐标点
            map_x, map_y, width, height = self.getMapUnitRect(last_pos[0], last_pos[1])
            purple_color = (255, 0, 255)# 紫色
            point_list = [(map_x, map_y), (map_x + width, map_y),
                          (map_x + width, map_y + height), (map_x, map_y + height)]
            # 多线绘制
            pygame.draw.lines(screen, purple_color, True, point_list, 1)# 在最后一步下的棋子绘制四方边框
    # 绘制棋盘与绘制黑点
    # 绘制15条水平和竖直的线，正中两条线加粗，然后在5个点上加上小正方形
    def drawBackground(self, screen):
        color = (0, 0, 0)
        for y in range(self.height):
            # draw a horizontal line
            # 双除号是取整的意思
            start_pos, end_pos = (REC_SIZE // 2, REC_SIZE // 2 + REC_SIZE * y), (
                MAP_WIDTH - REC_SIZE // 2, REC_SIZE // 2 + REC_SIZE * y)
            if y == (self.height) // 2:
                width = 2
            else:
                width = 1
            # 化线函数 颜色 初始点 结束点 线的宽度
            pygame.draw.line(screen, color, start_pos, end_pos, width)

        for x in range(self.width):
            # draw a horizontal line
            start_pos, end_pos = (REC_SIZE // 2 + REC_SIZE * x, REC_SIZE // 2), (
                REC_SIZE // 2 + REC_SIZE * x, MAP_HEIGHT - REC_SIZE // 2)
            if x == (self.width) // 2:
                width = 2
            else:
                width = 1
            pygame.draw.line(screen, color, start_pos, end_pos, width)

        rec_size = 12
        # 画出5个大黑点
        pos = [(3, 3), (11, 3), (3, 11), (11, 11), (7, 7)]
        for (x, y) in pos:
            pygame.draw.rect(screen, color,(
                REC_SIZE // 2 + x * REC_SIZE - rec_size // 2, REC_SIZE // 2 + y * REC_SIZE - rec_size // 2, rec_size,rec_size))

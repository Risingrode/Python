from ChessAI import *


class Button():
    def __init__(self, screen, text, x, y, color, enable):
        self.screen = screen
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT
        self.button_color = color
        self.text_color = (255, 255, 255)
        self.enable = enable
        self.font = pygame.font.SysFont(None, BUTTON_HEIGHT * 2 // 3)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topleft = (x, y)
        self.text = text
        self.init_msg()

    def init_msg(self):
        if self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
        else:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        if self.enable:
            self.screen.fill(self.button_color[0], self.rect)
        else:
            self.screen.fill(self.button_color[1], self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class StartButton(Button):
    def __init__(self, screen, text, x, y):
        super().__init__(screen, text, x, y, [(26, 173, 25), (158, 217, 157)], True)

    # 颜色改变函数
    def click(self, game):
        if self.enable:
            game.start()
            game.winner = None
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
            self.enable = False
            return True
        return False

    def unclick(self):
        if not self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
            self.enable = True


class GiveupButton(Button):
    def __init__(self, screen, text, x, y):
        super().__init__(screen, text, x, y, [(230, 67, 64), (236, 139, 137)], False)

    def click(self, game):
        if self.enable:
            game.is_play = False
            if game.winner is None:
                game.winner = game.map.reverseTurn(game.player)
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
            self.enable = False
            return True
        return False

    def unclick(self):
        if not self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
            self.enable = True


class Game():
    def __init__(self, caption):# 传入一个标题
        pygame.init()  # 先初始化游戏界面
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption(caption) # 这是游戏名字
        self.clock = pygame.time.Clock() # 创建时钟对象 (可以控制游戏循环频率)
        self.buttons = []
        # 下面这两个是基类
        self.buttons.append(StartButton(self.screen, 'Start', MAP_WIDTH + 30, 15))
        self.buttons.append(GiveupButton(self.screen, 'GiveUp', MAP_WIDTH + 30, BUTTON_HEIGHT + 45))
        self.is_play = False

        self.map = Map(CHESS_LEN, CHESS_LEN)
        self.player = MAP_ENTRY_TYPE.MAP_PLAYER_ONE
        self.action = None
        self.AI = ChessAI(CHESS_LEN)# 行数
        self.useAI = False
        self.winner = None

    # 初始化棋盘 游戏开始
    def start(self):
        self.is_play = True
        self.player = MAP_ENTRY_TYPE.MAP_PLAYER_ONE
        self.map.reset() # 初始化棋盘

    def play(self):
        self.clock.tick(60) # 每秒刷新60次
        light_yellow = (247, 238, 214)
        # 绘制黄色背景
        # Rect 函数格式：左上角坐标点 + 长和宽
        pygame.draw.rect(self.screen, light_yellow, pygame.Rect(0, 0, MAP_WIDTH, SCREEN_HEIGHT))
        # 把棋盘外面变成白色背景
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(MAP_WIDTH, 0, INFO_WIDTH, SCREEN_HEIGHT))
        # 绘制按钮
        for button in self.buttons:
            button.draw()
        # 正在玩游戏，并且没有结束
        if self.is_play and not self.isOver():
            if self.useAI:# AI在玩游戏
                x, y = self.AI.findBestChess(self.map.map, self.player)
                self.checkClick(x, y, True)
                self.useAI = False
            # 如果自己行动没有受限
            if self.action is not None:
                self.checkClick(self.action[0], self.action[1])
                self.action = None
            if not self.isOver():
                self.changeMouseShow()
        # 如果游戏结束了 就显示谁赢了
        if self.isOver():
            self.showWinner()
        # 绘制棋盘
        self.map.drawBackground(self.screen)
        # 贴棋子
        self.map.drawChess(self.screen)
    # 鼠标操作   绘制红色圆点
    def changeMouseShow(self):
        map_x, map_y = pygame.mouse.get_pos() # 选中坐标点
        x, y = self.map.MapPosToIndex(map_x, map_y) # 坐标点标准化
        # 如果这个点合法并且不为空
        if self.map.isInMap(map_x, map_y) and self.map.isEmpty(x, y):
            pygame.mouse.set_visible(False) # 隐藏光标
            light_red = (213, 90, 107)
            pos, radius = (map_x, map_y), CHESS_RADIUS
            # 在棋盘上画出一个可以随着鼠标移动的红色圆
            pygame.draw.circle(self.screen, light_red, pos, radius)
        else:
            pygame.mouse.set_visible(True)
    # 如果AI赢了，就让他赢，否则进入下一回合
    def checkClick(self, x, y, isAI=False):
        self.map.click(x, y, self.player)# 绘制棋子
        if self.AI.isWin(self.map.map, self.player):
            self.winner = self.player
            self.click_button(self.buttons[1])
        else:
            self.player = self.map.reverseTurn(self.player)
            # 把AI打开
            if not isAI:
                self.useAI = True
    # 获取当前人类点击坐标
    def mouseClick(self, map_x, map_y):
        if self.is_play and self.map.isInMap(map_x, map_y) and not self.isOver():
            x, y = self.map.MapPosToIndex(map_x, map_y)
            if self.map.isEmpty(x, y):
                self.action = (x, y)
    # 检测游戏是否结束
    def isOver(self):
        return self.winner is not None
    # 在屏幕上显示胜者
    def showWinner(self):
        def showFont(screen, text, location_x, locaiton_y, height):
            font = pygame.font.SysFont(None, height)
            font_image = font.render(text, True, (0, 0, 255), (255, 255, 255))
            font_image_rect = font_image.get_rect()
            font_image_rect.x = location_x
            font_image_rect.y = locaiton_y
            screen.blit(font_image, font_image_rect)

        if self.winner == MAP_ENTRY_TYPE.MAP_PLAYER_ONE:
            str = 'Winner is White'
        else:
            str = 'Winner is Black'
        showFont(self.screen, str, MAP_WIDTH + 25, SCREEN_HEIGHT - 60, 30)
        pygame.mouse.set_visible(True)
    # 使除该按钮外其他按钮关闭
    def click_button(self, button):
        if button.click(self):
            for tmp in self.buttons:
                if tmp != button:
                    tmp.unclick()
    # 检测点击位置是否在按钮上
    def check_buttons(self, mouse_x, mouse_y):
        for button in self.buttons:
            # 如果给定点位于矩形内，则返回true
            if button.rect.collidepoint(mouse_x, mouse_y):
                self.click_button(button)
                break


game = Game("FIVE CHESS " + GAME_VERSION)
while True:
    game.play()
    # 通过执行这个函数来让我们绘制的东西显示在屏幕上
    pygame.display.update()
    # 监测鼠标操作
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # 如果鼠标按下
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            game.mouseClick(mouse_x, mouse_y) # 把该点实例化到action数组中
            game.check_buttons(mouse_x, mouse_y)

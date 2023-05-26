import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenuBar, QMenu, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint

class ChessBoard:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_player = 1
        self.board = [[0 for _ in range(15)] for _ in range(15)]

    def play(self, row, col):
        if self.board[row][col] != 0:
            return False
        self.board[row][col] = self.current_player
        self.current_player = 3 - self.current_player
        return True

    def check_win(self):
        for i in range(15):
            for j in range(15):
                if self.board[i][j] == 0:
                    continue
                if j + 4 < 15 and self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == self.board[i][j+3] == self.board[i][j+4]:
                    return self.board[i][j] # 横向
                if i + 4 < 15 and self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == self.board[i+3][j] == self.board[i+4][j]:
                    return self.board[i][j] # 竖向
                if i + 4 < 15 and j + 4 < 15 and self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3] == self.board[i+4][j+4]:
                    return self.board[i][j] # 右斜向
                if i + 4 < 15 and j - 4 >= 0 and self.board[i][j] == self.board[i+1][j-1] == self.board[i+2][j-2] == self.board[i+3][j-3] == self.board[i+4][j-4]:
                    return self.board[i][j] # 左斜向
        return 0

class ChessBoardWidget(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.board = ChessBoard()
        self.setMinimumSize(600, 600)
        self.setMaximumSize(600, 600)
        self.setMouseTracking(True)
        self.reset()

    def reset(self):
        self.board.reset()
        self.winner = 0
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(QPen(Qt.black, 2))
        for i in range(15):
            painter.drawLine(20, 20 + i * 40, 580, 20 + i * 40) # 画横线
            painter.drawLine(20 + i * 40, 20, 20 + i * 40, 580) # 画竖线
        painter.setPen(QPen(Qt.black, 3))
        for i in range(15):
            for j in range(15):
                if self.board.board[i][j] == 1:
                    painter.setBrush(Qt.black)
                    painter.drawEllipse(QPoint(20 + j * 40, 20 + i * 40), 18, 18) # 画黑子
                elif self.board.board[i][j] == 2:
                    painter.setBrush(Qt.white)
                    painter.drawEllipse(QPoint(20 + j * 40, 20 + i * 40), 18, 18) # 画白子

    def mousePressEvent(self, event):
        if self.winner != 0:
            return
        if event.button() == Qt.LeftButton:
            col = (event.x() - 20) // 40
            row = (event.y() - 20) // 40
            if col < 0 or col >= 15 or row < 0 or row >= 15:
                return
            if not self.board.play(row, col):
                return
            self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("五子棋")
        self.setCentralWidget(ChessBoardWidget(self))
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("文件")
        new_game_action = QAction(QIcon(), "新游戏", self)
        new_game_action.triggered.connect(self.new_game)
        file_menu.addAction(new_game_action)

    def new_game(self):
        self.centralWidget().reset()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

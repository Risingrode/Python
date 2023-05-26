import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt


class Chessboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 450, 450)
        self.setWindowTitle('五子棋')

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.board = QFrame()
        self.board.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.board.setStyleSheet("background-color: rgb(240, 217, 181)")
        layout.addWidget(self.board)

        self.board.installEventFilter(self)

    def eventFilter(self, watched, event):
        if watched == self.board:
            if event.type() == QEvent.Paint:
                self.drawBoard()

        return super().eventFilter(watched, event)

    def drawBoard(self):
        painter = QPainter(self.board)
        painter.setPen(QPen(QColor(Qt.black), 2))

        # 画棋盘
        for i in range(15):
            painter.drawLine(15 + i * 30, 15, 15 + i * 30, 435)
            painter.drawLine(15, 15 + i * 30, 435, 15 + i * 30)
        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chessboard = Chessboard()
    chessboard.show()
    sys.exit(app.exec_())

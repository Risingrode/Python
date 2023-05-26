# demo2_1Hello.py
# 使用PyQt6，纯代码化创建一个简单的GUI程序
# 4.10日
import sys
from PyQt6 import QtCore, QtGui, QtWidgets

# 创建app， 用QApplication类
app = QtWidgets.QApplication(sys.argv)
# 创建窗体，用QWidget类
widgetHello = QtWidgets.QWidget()
# 设置窗体的宽度和高度
widgetHello.resize(280, 150)
# 设置窗体的标题文字
widgetHello.setWindowTitle("Demo2_1")
# 创建标签，父容器为widgetHello
LabHello = QtWidgets.QLabel(widgetHello)
# 设置标签文字
LabHello.setText("Hello World, PyQt6")
# 设置字体对象font, 用QFont类
font = QtGui.QFont()
# 设置字体大小
font.setPointSize(12)
# 设置为粗体

font.setBold(True)
# 设置为标签LabHello的字体
LabHello.setFont(font)
# 获取LabHello的合适大小，返回值是QSize类对象
size = LabHello.sizeHint()
LabHello.setGeometry(70, 60, size.width(), size.height())
# 显示对话框
widgetHello.show()
# 应用程序运行
sys.exit(app.exec())
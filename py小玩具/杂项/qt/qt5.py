# 导入必要的模块
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QSlider, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

# 创建应用程序对象
app = QApplication(sys.argv)

# 创建窗口对象
window = QWidget()

# 设置窗口大小
window.resize(500, 500)

# 设置窗口标题
window.setWindowTitle('音乐播放器')

# 创建标签对象
label = QLabel(window)
label.setText('No music selected')
label.setAlignment(Qt.AlignCenter)

# 创建按钮对象
open_button = QPushButton('Open', window)
play_button = QPushButton('Play', window)
pause_button = QPushButton('Pause', window)
stop_button = QPushButton('Stop', window)

# 创建滑动条对象
slider = QSlider(Qt.Horizontal, window)

# 创建水平布局对象
h_box = QHBoxLayout()
h_box.addWidget(open_button)
h_box.addWidget(play_button)
h_box.addWidget(pause_button)
h_box.addWidget(stop_button)

# 创建垂直布局对象
v_box = QVBoxLayout()
v_box.addWidget(label)
v_box.addWidget(slider)
v_box.addLayout(h_box)

# 设置窗口布局
window.setLayout(v_box)

# 创建媒体播放器对象
player = QMediaPlayer()

# 打开文件
def open_file():
    file_path, _ = QFileDialog.getOpenFileName(window, 'Open Music File', '', 'MP3 Files (*.mp3);;All Files (*)')
    if file_path:
        label.setText(file_path.split('/')[-1])
        player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        player.durationChanged.connect(set_duration)
        player.positionChanged.connect(set_position)
        player.stateChanged.connect(set_state)

# 播放音乐
def play_music():
    player.play()

# 暂停音乐
def pause_music():
    player.pause()

# 停止音乐
def stop_music():
    player.stop()

# 设置音乐总时长
def set_duration():
    slider.setMaximum(player.duration())

# 设置音乐当前播放时间
def set_position():
    slider.setValue(player.position())

# 设置音乐播放状态
def set_state(state):
    if state == QMediaPlayer.StoppedState:
        player.setPosition(0)
        slider.setValue(0)

# 绑定按钮事件
open_button.clicked.connect(open_file)
play_button.clicked.connect(play_music)
pause_button.clicked.connect(pause_music)
stop_button.clicked.connect(stop_music)
slider.sliderMoved.connect(player.setPosition)

# 显示窗口
window.show()

# 进入应用程序的主循环
sys.exit(app.exec_())


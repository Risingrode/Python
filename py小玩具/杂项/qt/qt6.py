# 导入必要的模块
from PyQt5.QtMultimedia import QMediaContent
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider,
                             QStyle, QVBoxLayout, QWidget,QFileDialog)

# 创建应用程序
app = QApplication([])

# 创建主窗口
window = QWidget()
window.setWindowTitle("音乐播放器")
# window.setWindowIcon(QIcon('/d:/Cursor/杂项/python/pyQt5/music.png'))

# 创建媒体播放器
player = QMediaPlayer()

# 创建标签
label = QLabel()
label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

# 创建播放/暂停按钮
play_button = QPushButton()
play_button.setEnabled(False)
play_button.setIcon(QIcon.style().standardIcon(QStyle.SP_MediaPlay))

# 创建进度条
position_slider = QSlider(Qt.Horizontal)
position_slider.setRange(0, 0)
position_slider.sliderMoved.connect(player.setPosition)

# 创建音量控制条
volume_slider = QSlider(Qt.Horizontal)
volume_slider.setRange(0, 100)
volume_slider.setValue(100)
volume_slider.sliderMoved.connect(player.setVolume)

# 创建布局
control_layout = QHBoxLayout()
control_layout.setContentsMargins(0, 0, 0, 0)
control_layout.addWidget(play_button)
control_layout.addWidget(position_slider)

layout = QVBoxLayout()
layout.addWidget(label)
layout.addLayout(control_layout)
layout.addWidget(volume_slider)

# 设置主窗口布局
window.setLayout(layout)

# 打开音乐文件
def open_file():
    file_name, _ = QFileDialog.getOpenFileName(window, "打开文件", ".", "音乐文件 (*.mp3 *.wav)")
    if file_name != '':
        player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
        play_button.setEnabled(True)

# 播放/暂停音乐
def play_music():
    if player.state() == QMediaPlayer.State.PlayingState:
        player.pause()
    else:
        player.play()

# 更新标签和进度条
def update_label():
    duration = player.duration()
    if duration > 0:
        position_slider.setMaximum(duration)
        seconds = duration / 1000
        minutes = seconds / 60
        seconds -= minutes * 60
        label.setText("%d:%02d" % (minutes, seconds))

# 更新播放/暂停按钮图标
def update_play_button():
    if player.state() == QMediaPlayer.State.PlayingState:
        play_button.setIcon(QIcon.style().standardIcon(QStyle.SP_MediaPause))
    else:
        play_button.setIcon(QIcon.style().standardIcon(QStyle.SP_MediaPlay))

# 更新进度条位置
def update_position_slider(position):
    position_slider.setValue(position)

# 更新音量控制条位置
def update_volume_slider(volume):
    volume_slider.setValue(volume)

# 连接信号和槽
player.durationChanged.connect(update_label)
player.positionChanged.connect(update_position_slider)
player.stateChanged.connect(update_play_button)
player.volumeChanged.connect(update_volume_slider)

play_button.clicked.connect(play_music)

# 打开文件
open_file()

# 显示主窗口
window.show()

# 运行应用程序
app.exec()
import tkinter as tk
from tkinter import *
import os, threading, pygame
import tkinter.messagebox as msgbox
import tkinter.filedialog


class KgyySpider(object):
    def __init__(self):
        # 新建窗口
        self.user_input_data = None
        self.window = tk.Tk()
        self.window.title('酷狗音乐采集助手 - Fcw')
        self.window.resizable(False, False)
        # 3、设置窗口大小和居中
        x = int((self.window.winfo_screenwidth() / 2) - (800 / 2))
        y = int((self.window.winfo_screenheight() / 2) - (600 / 2))
        self.window.geometry('{}x{}+{}+{}'.format(720, 500, x, y))
        # 4、创建提示话语标语标签
        self.prompt_words_2 = tk.Label(self.window, text='选择想要听的音乐序号', font=('Kaiti', 12), width=10,
                                       height=2, )
        self.prompt_words_2.grid(row=1, column=1, pady=1, sticky=W + E + N + S, padx=20)
        self.prompt_words_2 = Variable()
        # 5、创建用户输入标签
        self.user_input = tk.Entry(self.window, show=None, font=('Kaiti', 12), textvariable=self.prompt_words_2)
        self.user_input.grid(row=2, column=1, sticky=W + E + N + S, padx=20)

        self.start_button = tk.Button(self.window, text='开始', font=('Kaiti', 12), width=10, height=1,
                                      command=self.main)
        self.start_button.grid(row=4, column=1, pady=10, sticky=W + E + N + S, padx=20)
        # B、清屏按钮
        self.clear_button = tk.Button(self.window, text='清屏', font=('Kaiti', 12), width=10, height=1,
                                      command=self.clear)
        self.clear_button.grid(row=19, column=1, pady=10, sticky=W + N + S, padx=10)
        # C、退出按钮
        self.quit_button = tk.Button(self.window, text='退出', font=('Kaiti', 12), width=10, height=1,
                                     command=self.quit)
        self.quit_button.grid(row=19, column=1, pady=10, sticky=E + N + S, padx=10)
        # 7、创建富文本框，用于打印提示性话语
        self.text_box = tk.Text(self.window, font=('Kaiti', 12), width=60, height=30)
        self.text_box.grid(row=0, column=2, rowspan=20, columnspan=20, sticky=W + E + N + S, padx=5, pady=5)
        # 8、创建滚轮条标签
        self.scroll = tk.Scrollbar(orient="vertical", command=self.text_box)
        self.scroll['command'] = self.text_box.yview()
        self.scroll.grid(row=0, column=29, rowspan=20, columnspan=2, sticky=S + W + E + N, padx=5, pady=5)
        # 9、富文本框提示语句
        self.text_box.insert("insert", '****************欢迎使用下载小程序(阿威版^_^)***************' + '\n')
        self.text_box.insert("insert", '\n' + '\n')
        # 18.播放按钮
        self.play_button = tk.Button(self.window, text='播放', font=('Kaiti', 12), width=10, height=1,
                                     command=self.PlayMusic)
        self.play_button.grid(row=12, column=1, pady=10, sticky=W + N + S, padx=10)
        # 音乐路径
        self.music_path = []
        self.path = []

    # 音乐播放
    def PlayMusic(self):
        if len(self.path) == 0:
            self.path = tkinter.filedialog.askdirectory()
            self.music_path = [self.path + '/' + x for x in os.listdir(self.path) if x.endswith(".mp3")]
            self.showMusicList()
        else:
            self.choice()

    # 弹窗
    def PopWin(self, target):
        answer = msgbox.askokcancel('提示', target)

    def showMusicList(self):
        i = 0
        for x in os.listdir(self.path):
            i += 1
            self.text_box.insert("insert", '序号是:{}:音乐是：{}'.format(i, x + "\n"))
        self.choice()

    # 音乐播放
    def choice(self):
        num = int(self.user_input.get())
        pygame.mixer.init()
        if num:
            self.play(num)
        else:
            self.PopWin('懒得写，不咋会！')
        # pygame.mixer.music.load(str(self.music_path[num - 1]))
        # for i in range(num + 2, len(self.music_path) + 1):  # 左闭右开
        #      pygame.mixer.music.queue(str(self.music_path[i - 1]))
        #     pygame.mixer.music.play(0)  # 0表示不循环，-1表示无限循环，设置1表示循环一次，即一共播放两次
        #    while pygame.mixer.music.get_busy():  # 在音频播放为完成之前不退出程序
        #       pass

    def play(self, num):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(str(self.music_path[num - 1]))
        pygame.mixer.music.play()

    def clear(self):
        self.text_box.delete("1.0", "end")

    def quit(self):
        self.window.quit()

    def main(self):
        Running = threading.Thread(target=self.user_input_data)
        Running.daemon = True
        Running.start()


if __name__ == '__main__':
    kgyy = KgyySpider()
    kgyy.window.mainloop()

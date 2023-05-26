import tkinter as tk
from tkinter import *

from tkinter import ttk

from . import ui_tools


class MainUi(tk.TK):
    def __init__(self):
        # 参数
        super().__init__()  # 有点相当于tk.Tk()
        self.showLabel = tk.StringVar()  # 标签显示
        self.user_input = tk.StringVar()  # 歌手
        self.musicNum = tk.StringVar()  # 选择的音乐序号

        self.btn_ok = ttk.Button()  # 是否按下按钮
        self.start_button = ttk.Button()
        self.clear_button = ttk.Button()
        self.quit_button = ttk.Button()
        self.text_box = tk.StringVar()
        self.scroll = tk.Text()
        self.input_num = tk.StringVar()

        self.download_button = ttk.Button()
        self.download_path = ttk.Button()
        self.play_button = ttk.Button()

        self.lb=tk.Label()

        self.mainWin()  # 调用主窗口

    # 音乐播放实例化
    def mainWin(self):
        '''
        mainmenu = Menu(self)
        menuFile = Menu(mainmenu)
        mainmenu.add_cascade(label='菜单', menu=menuFile)
        menuFile.add_command(label='新窗体', command=self2)
        menuFile.add_separator()
        menuFile.add_command(label='退出', command=self.destroy)
        self.config(menu=mainmenu)
        # self.mainloop()
        '''

        # self.title('酷狗音乐采集助手 - Fcw')
        # 2、禁止修改窗口大小
        self.resizable(False, False)
        # 3、设置窗口大小和居中
        x = int((self.winfo_screenwidth() / 2) - (800 / 2))
        y = int((self.winfo_screenheight() / 2) - (600 / 2))
        self.geometry('{}x{}+{}+{}'.format(720, 500, x, y))
        # 4、标签
        tk.Label(self, text="请输入歌手名称", font=('Kaiti', 12), width=10, height=2).grid(row=0, column=1, pady=1,
                                                                                           sticky=W + E + N + S,
                                                                                           padx=20)
        tk.Label(self, text='如: 周杰伦, 林俊杰', font=('Kaiti', 12), width=10, height=2).grid(row=1, column=1, pady=1,
                                                                                               sticky=W + E + N + S,
                                                                                               padx=20)  # padx=20
        # 5、输入歌手名
        tk.Entry(self, show=None, font=('Kaiti', 12), textvariable=self.user_input).grid(row=2, column=1,
                                                                                         sticky=W + E + N + S, padx=20)
        # 6、设置点击开始运行点击按钮
        # A、main
        self.start_button = tk.Button(self, text='开始', font=('Kaiti', 12), width=10, height=1)
        self.start_button.grid(row=4, column=1, pady=10, sticky=W + E + N + S, padx=20)
        # B、clear
        self.clear_button = tk.Button(self, text='清屏', font=('Kaiti', 12), width=10, height=1)
        self.clear_button.grid(row=19, column=1, pady=10, sticky=W + N + S, padx=10)
        # C、quit
        self.quit_button = tk.Button(self, text='退出', font=('Kaiti', 12), width=10, height=1, )
        self.quit_button.grid(row=19, column=1, pady=10, sticky=E + N + S, padx=10)
        # 7、创建富文本框，用于打印提示性话语
        self.text_box = tk.Text(self, font=('Kaiti', 12), width=60, height=30)
        self.text_box.grid(row=0, column=2, rowspan=20, columnspan=20, sticky=W + E + N + S, padx=5, pady=5)
        # 8、创建滚轮条标签
        self.scroll = tk.Scrollbar(orient="vertical", command=self.text_box)
        self.scroll['command'] = self.text_box.yview()
        self.scroll.grid(row=0, column=29, rowspan=20, columnspan=2, sticky=S + W + E + N, padx=5, pady=5)
        # 9、富文本框提示语句
        self.text_box.insert("insert", '****************欢迎使用下载小程序(阿威版^_^)***************' + '\n')
        self.text_box.insert("insert", '\n' + '\n')

        # 10、爬虫初始化变量
        '''
        self.session = HTMLSession()
        self.cookies_dfid = '34dZ1w4Y0yX40RzxhP3irRmF'
        self.cookies_mid = '0f0f5f52283297b26e8d1a84be3c5999'
        self.start_url = r'https://complexsearch.kugou.com/v2/search/song?'
        self.song_info_url = r'https://wwwapi.kugou.com/yy/index.php?'
        '''
        # 12.选择输入框
        self.input_num = tk.Entry(self, show=None, font=('Kaiti', 12), textvariable=self.musicNum)
        self.input_num.grid(row=6, column=1, sticky=W + E + N + S, padx=10)
        # 13.下载按钮
        self.download_button = tk.Button(self, text='下载', font=('Kaiti', 12), width=10, height=1)
        self.download_button.grid(row=9, column=1, pady=10, sticky=W + N + S, padx=10)
        # 14.下载说明
        tk.Label(self, text='输入音乐序号进行下载', font=('Kaiti', 12), width=10,
                                       height=2).grid(row=8, column=1, pady=1, sticky=W + E + N + S, padx=10)
        # 15.一键下载
        self.download_button = tk.Button(self, text='下载全部', font=('Kaiti', 12), width=10, height=1)
        self.download_button.grid(row=9, column=1, pady=10, sticky=E + N + S, padx=10)
        # 16.弹出框
        self.lb = tk.Label(self, text='')
        # 17.选择下载地址 downAll
        self.download_path = tk.Button(self, text='下载地址选择', font=('Kaiti', 12), width=10, height=1)
        self.download_path.grid(row=10, column=1, pady=10, sticky=W + N + S + E, padx=10)
        # 18.播放按钮 PlayMusic
        self.play_button = tk.Button(self, text='播放', font=('Kaiti', 12), width=10, height=1)
        self.play_button.grid(row=12, column=1, pady=10, sticky=W + N + S, padx=10)
        ui_tools.WinCenter(self)
        # 第二个窗口

    def Window2(self):
        winNew = Toplevel(self)
        winNew.geometry('320x240')
        winNew.title('新窗体')
        lb2 = Label(winNew, text='我在新窗体上')
        lb2.place(relx=0.2, rely=0.2)
        btClose = Button(winNew, text='关闭', command=winNew.destroy)
        btClose.place(relx=0.7, rely=0.5)


if __name__ == '__main__':
    Ui = MainUi()
    Ui.title('酷狗音乐采集助手 - Fcw')

    Ui.mainloop()

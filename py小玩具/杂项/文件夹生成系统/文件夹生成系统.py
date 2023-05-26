import tkinter as tk
from tkinter import *
import os, xlrd
import tkinter.messagebox as msgbox
import tkinter.filedialog


class File(object):
    def __init__(self):
        # 新建窗口
        self.window = tk.Tk()
        mainmenu = Menu(self.window)
        menuFile = Menu(mainmenu)
        mainmenu.add_cascade(label='菜单', menu=menuFile)
        menuFile.add_command(label='关于作者', command=self.Window2)
        menuFile.add_separator()
        menuFile.add_command(label='退出', command=self.window.destroy)
        self.window.config(menu=mainmenu)

        self.window.title('文件夹生成系统plus - 1.0')
        self.window.resizable(False, False)
        x = int((self.window.winfo_screenwidth() / 2) - (800 / 2))
        y = int((self.window.winfo_screenheight() / 2) - (600 / 2))
        self.window.geometry('{}x{}+{}+{}'.format(720, 500, x, y))

        self.clear_button = tk.Button(self.window, text='清屏', font=('Kaiti', 12), width=20, height=1,
                                      command=self.clear)
        self.clear_button.grid(row=19, column=1, pady=10, sticky=W + N + S, padx=10)

        self.quit_button = tk.Button(self.window, text='退出', font=('Kaiti', 12), width=20, height=1,
                                     command=self.quit)
        self.quit_button.grid(row=18, column=1, pady=10, sticky=E + N + S, padx=10)

        self.text_box = tk.Text(self.window, font=('Kaiti', 12), width=60, height=30)
        self.text_box.grid(row=0, column=2, rowspan=20, columnspan=20, sticky=W + E + N + S, padx=5, pady=5)

        self.showText()

        self.Lend = tk.Button(self.window, text='导入学号', font=('Kaiti', 12), width=20, height=1,
                              command=self.importNum)
        self.Lend.grid(row=8, column=1, pady=10, sticky=W + N + S + E, padx=10)

        self.lb = tk.Label(self.window, text='')  # 弹出第二个框

        self.Lend = tk.Button(self.window, text='导入姓名', font=('Kaiti', 12), width=20, height=1,
                              command=self.importName)
        self.Lend.grid(row=9, column=1, pady=10, sticky=W + N + S + E, padx=10)

        self.Lend = tk.Button(self.window, text='选择保存到文件夹', font=('Kaiti', 12), width=20, height=1,
                              command=self.SavePath)
        self.Lend.grid(row=10, column=1, pady=10, sticky=W + N + S + E, padx=10)

        self.Lend = tk.Button(self.window, text='一键生成', font=('Kaiti', 12), width=20, height=1,
                              command=self.productFile)
        self.Lend.grid(row=11, column=1, pady=10, sticky=W + N + S + E, padx=10)

        self.name = Variable()


        self.AllNum = []  # 所有学号
        self.numPath = ''
        self.AllPerson = []  # 班级所有人员姓名
        self.personPath = ''
        self.savePath = ''  # 保存路径
        self.EndName = []  # 拼接好的名字

    # 第二个窗口
    def Window2(self):
        winNew = Toplevel(self.window)
        winNew.geometry('320x240')
        winNew.title('关于作者')
        lb2 = Label(winNew, text='软件是我两天开发出来的，以后更不更新看心情^_^！')
        lb3 = Label(winNew, text='如果有啥更新建议，请发邮箱3377078894@qq.com')
        lb2.place(relx=0, rely=0.2)
        lb3.place(relx=0, rely=0.4)
        btClose = Button(winNew, text='关闭', command=winNew.destroy)
        btClose.place(relx=0.7, rely=0.5)

    # 弹窗
    def PopWin(self, target):
        answer = msgbox.askokcancel('提示', target)
        if answer:
            self.lb.config(text='已确认')
        else:
            self.lb.config(text='已取消')

    # 开局提示
    def showText(self):
        self.text_box.insert("insert", '****************欢迎使用文件筛选系统(fcw版^_^)*************' + '\n')
        self.text_box.insert("insert", '说明：' + '\n')
        self.text_box.insert("insert", '1.点击一键导入' + '\n')
        self.text_box.insert("insert",
                             '2.弹出一个文件选择框，导入你们班人员学号' + '\n')
        self.text_box.insert("insert",
                             '3.再弹出一个文件选择框，导入你们班人员姓名' + '\n')
        self.text_box.insert("insert",
                             '4.选择保存路径 每开一下只能用一次，想用第二次的话只能关闭再打开，主要是不想写了' + '\n')

    # 导入学号
    def importNum(self):
        self.numPath = tkinter.filedialog.askopenfilename()  # 获取文件路径
        with open(str(self.numPath), "r", encoding='utf-8') as f:
            data = f.readlines()
        for i in data:  # 导入学号
            if i != '':
                p = i[:-1]
                self.AllNum.append(p)
        self.PopWin("导入学号成功")

    # 导入姓名
    def importName(self):
        self.personPath = tkinter.filedialog.askopenfilename()
        with open(str(self.personPath), "r", encoding='utf-8') as f:
            data = f.readlines()
        for i in data:  # 导入姓名
            if i != '':
                p = i[:-1]
                self.AllPerson.append(p)
        self.PopWin("导入姓名成功")

    def linkName(self):
        for i, j in zip(self.AllNum, self.AllPerson):# zip函数用于for中的2个对象
            self.EndName.append(i+j)

    def productFile(self):
        self.linkName()  # 拼接
        for val in self.EndName:
            path = str(self.savePath+'/' + str(val))
            os.makedirs(path)
        self.PopWin("生成成功！")

    def SavePath(self):
        self.savePath = tkinter.filedialog.askdirectory()
        self.PopWin("导入文件路径成功")
        # print(self.savePath)


    def clear(self):
        self.text_box.delete("1.0", "end")

    def quit(self):
        self.window.quit()


if __name__ == '__main__':
    file = File()
    file.window.mainloop()

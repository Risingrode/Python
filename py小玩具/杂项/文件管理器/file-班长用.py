import tkinter as tk
from tkinter import *
import os
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

        self.window.title('查找系统 - 班长专属')
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

        self.Lend = tk.Button(self.window, text='谁健康码截图没交？', font=('Kaiti', 12), width=20, height=1,
                              command=self.writeOk)
        self.Lend.grid(row=8, column=1, pady=10, sticky=W + N + S + E, padx=10)
        #
        self.Lend = tk.Button(self.window, text='谁核酸没接龙？', font=('Kaiti', 12), width=20, height=1,
                              command=self.ZuoHeSuanOk)
        self.Lend.grid(row=10, column=1, pady=10, sticky=W + N + S + E, padx=10)

        self.lb = tk.Label(self.window, text='')  # 弹出第二个框

        self.name = Variable()
        self.geshi = Variable()
        # self.banji = Variable()
        # 筛选格式
        # self.GeShi = tk.Entry(self.window, show='计2nb', font=('Kaiti', 12), textvariable=self.geshi)  # show表示加密
        # self.GeShi.grid(row=6, column=1, sticky=W + E + N + S, padx=10)

        self.AllPerson = []  # 班级所有人员姓名
        self.OkPerson = []  # 已交成员姓名
        self.OkPersonNoGeShi = []  # 未格式化的已交成员姓名
        self.NoPerson = []  # 未交成员姓名
        self.Person = []  # 未筛选前的已交人员
        self.OkPath = []  # 已交作业的文件夹
        self.AllNum = []
        self.AllLong = []  # 所有接龙人员
        self.JieLong = 0

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
        self.text_box.insert("insert", '1.弹出第一个文件选择框，导入你们班所有人员名单，格式是：一人名字占一行' + '\n')
        self.text_box.insert("insert",
                             '2.弹出第二个文件选择框，导入你们班健康码的文件夹' + '\n')
        self.text_box.insert("insert",
                             '3.第二个按钮（做核酸检测），先把接龙人员名字写到一个txt中即可，再导入接龙文本（txt）文件。' + '\n')

    # 找到txt文件路径
    def writeOk(self):
        self.clearText()  # 先清理一下
        self.Person = tkinter.filedialog.askopenfilename()
        if self.Person:
            self.PopWin("存入同学名称成功！")
            self.createOk()
        else:
            self.PopWin("请找到正确文件夹！")

    def clearText(self):
        del self.AllPerson[:]  # 班级所有人员姓名
        del self.OkPerson[:]  # 已交成员姓名
        del self.OkPersonNoGeShi[:]  # 未格式化的已交成员姓名
        del self.NoPerson[:]  # 未交成员姓名
        del self.Person[:]  # 未筛选前的已交人员
        del self.OkPath[:]  # 已交作业的文件夹
        del self.AllNum[:]
        # self.JieLong = 0

    # 读取txt文件
    def createOk(self):
        if self.JieLong == 0:
            self.OkPath = tkinter.filedialog.askdirectory()  # 找到已交健康码人员
            # self.Person 全班人员txt路径
            with open(str(self.Person), "r", encoding='utf-8') as f:
                data = f.readlines()
            for i in data:
                if i != '':
                    p = i[:-1]
                    self.AllPerson.append(p)
        else:
            self.JieLongTxt()
            return

            # 筛选特定格式文件
        self.Person = [x for x in os.listdir(str(self.OkPath))]

        for j in self.Person:
            if j.endswith('.jpg') or j.endswith('.png'):
                self.OkPersonNoGeShi.append(j)
        # self.OkPersonNoGeShi  所有文件格式

        self.removeFile()

    # 筛选没有接龙的
    def ZuoHeSuanOk(self):
        self.JieLong = 1
        self.writeOk()

    def JieLongTxt(self):
        with open(str(self.Person), "r", encoding='utf-8') as f:
            data = f.readlines()
        for i in data:
            if i != '':
                p = i[:-1]
                self.AllPerson.append(p)
        # print(self.AllPerson)
        self.OkPath = tkinter.filedialog.askopenfilename()
        with open(str(self.OkPath), "r", encoding='utf-8') as f:
            data = f.readlines()
        for i in data:
            if i != '':
                p = i[:-1]
                self.OkPerson.append(p)

        for i in self.AllPerson:
            flag = 1
            for j in self.OkPerson:
                if i in j:
                    flag = 0
            if flag:
                self.NoPerson.append(i)
        self.showNoPerson()

    # 对传过来的不规则数据进行筛选
    def removeFile(self):
        for i in self.OkPersonNoGeShi:
            for j in self.AllPerson:
                if j in i:
                    self.OkPerson.append(j)

        for i in self.AllPerson:
            flag = 1
            for j in self.OkPerson:
                if i == j:
                    flag = 0
            if flag:
                self.NoPerson.append(i)

        self.showNoPerson()

    def showNoPerson(self):
        self.text_box.insert("insert", '未交人员总计: {}'.format(len(self.NoPerson)) + "\n")
        for i in self.NoPerson:
            self.text_box.insert("insert", '未交: {}'.format(i) + "\n")
        self.JieLong = 0

    def clear(self):
        self.text_box.delete("1.0", "end")

    def quit(self):
        self.window.quit()


if __name__ == '__main__':
    file = File()
    file.window.mainloop()

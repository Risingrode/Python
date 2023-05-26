import cmath
import math
import os
import numpy as np
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox as msgbox
from tkinter import *

import nums_from_string
from PIL import Image, ImageTk
np.set_printoptions(suppress=True)

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

        self.window.title('数据计算系统plus - 2.0')
        self.window.resizable(False, False)
        x = int((self.window.winfo_screenwidth() / 2) - (800 / 2))
        y = int((self.window.winfo_screenheight() / 2) - (600 / 2))
        self.window.geometry('{}x{}+{}+{}'.format(1000, 600, x, y))  # 主窗口大小

        self.clear_button = tk.Button(self.window, text='清屏', font=('Kaiti', 12), width=20, height=1,
                                      command=self.clear)
        self.clear_button.grid(row=20, column=0, pady=10, sticky=W + E + N + S, padx=10)

        self.quit_button = tk.Button(self.window, text='退出', font=('Kaiti', 12), width=20, height=1,
                                     command=self.quit)
        self.quit_button.grid(row=19, column=0, pady=10, sticky=W + E + N + S, padx=10)

        self.text_box = tk.Text(self.window, font=('Kaiti', 12), width=60, height=30)  # 这里是大的文本框
        self.text_box.grid(row=0, column=3, rowspan=20, columnspan=20, sticky=W + E + N + S, padx=5, pady=5)
        self.showText() # 调用这个函数，给右边的那个文本框显示文字

        self.Lend = tk.Button(self.window, text='导入数据(txt)', font=('Kaiti', 12), width=20, height=1,
                              command=self.importData)
        self.Lend.grid(row=18, column=0, pady=10, sticky=W + N + S + E, padx=10)

        self.E0 = Variable()  # 初始值
        self.Ei = Variable()  # 迭代量
        self.E0 = tk.Entry(self.window, show='', font=('Kaiti', 12), textvariable=self.E0)  # show表示加密
        self.E0.grid(row=4, column=0, sticky=W + E + N + S, padx=10)
        self.E0.insert(0, '请输入断裂能初始值')
        self.Ei = tk.Entry(self.window, show='', font=('Kaiti', 12), textvariable=self.Ei)  # show表示加密
        self.Ei.grid(row=6, column=0, sticky=W + E + N + S, padx=10)
        self.Ei.insert(0, '请输入迭代增量')

        self.lb = tk.Label(self.window, text='')  # 弹出第二个框

        # 贴图片
        self.img_open = Image.open('1.png')  # 前面图片
        self.img_png = ImageTk.PhotoImage(self.img_open)
        # 创建一个Label标签，将图片贴上去
        self.label_img = tk.Label(self.window, image=self.img_png)
        self.label_img.config(width=435, height=156)
        self.label_img.grid(row=10, column=0, sticky=W + E + N + S, padx=8, pady=0)

        self.imgpgo = Image.open('2.png')  # 后面图片
        self.imgpg = ImageTk.PhotoImage(self.imgpgo)
        self.labelimg = tk.Label(self.window, image=self.imgpg)
        self.labelimg.config(width=464, height=84)
        self.labelimg.grid(row=15, column=0, sticky=W + E + N + S, padx=30, pady=10)

        self.KeyData = []  # 表1数据
        self.Data = []
        self.txt_contents = []  # 所有数据
        self.KeyPath = ''
        self.DataPath = ''
        self.E = 0  # 能量标记
        self.area = 0  # 表一截面积
        self.num = 0  # 表一数据量
        self.area1 = 0  # 截面积
        self.num1 = 0  # 数据量
        self.ans = 0  # 每一层的F1
        self.res = 0  # 真正的结果

    # 第二个窗口
    def Window2(self):
        winNew = Toplevel(self.window)
        winNew.geometry('320x240')
        winNew.title('关于作者')
        lb2 = Label(winNew, text='软件是我好几天开发出来的，给的数据也不太行，呜呜呜~~~~，以后更不更新看心情^_^！')
        lb3 = Label(winNew, text='如果有啥更新建议，请发邮箱YANYUBINGSHANG@outlook.com')
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
        self.text_box.insert("insert", '****************欢迎使用数据计算系统(fcw版^_^)*************' + '\n')
        self.text_box.insert("insert", '说明：' + '\n')

        self.text_box.insert("insert", '请按左边图片所示格式处理您的数据' + '\n')
        self.text_box.insert("insert",
                             '输入文件数据及其数据单位' + '\n' + '横截面积 A mm²' + '\n' + '负荷 f KN' + '\n' + '根拉伸位移 D mm' + '\n')
        self.text_box.insert("insert",
                             '关于程序内字母说明及其单位 ' + '\n' + 'Wr 断裂能 KN·mm' + '\n' + 'Cr 根的附加粘聚力 KN/mm²' + '\n')
        self.text_box.insert("insert",
                             '导入文件时,把所有数据存到一个文件夹里' + '\n' + '导入该文件夹即可' + '\n')

    # 导入数据  数量联系
    def importData(self):
        txt_list = []  # 用于存储读取的txt内容
        self.DataPath = tkinter.filedialog.askdirectory()  # 获取文件路径
        # 获取文件夹下所有txt文件的文件名    按照字典排序进行读取的
        txt_files = [f for f in os.listdir(self.DataPath) if f.endswith('.txt')]
        NUM = len(txt_files)  # 根的数量
        # print(NUM)
        # print("狗蛋")
        # print(txt_files)  # txt文本文档获取成功
        # print(len(txt_files)) # 个数合适，一个不漏

        res_file = 'D:\\resultNum.txt'
        with open(res_file, "w") as file:
            str = "结果如下："
            file.write(str + "\n")
        Ek = float(self.E0.get()) / NUM  # 拿到分量

        # TODO:
        AreaSum = 0  # 总的面积
        areaSum = []  # 存储所有面积
        # 下面函数是求所有面积和的
        for i in range(len(txt_files)):
            Path1 = self.DataPath + '/' + txt_files[i]
            with open(Path1, 'r', encoding='gbk') as file1:
                content1 = file1.readlines()
            # print(content1[3])
            pNum = nums_from_string.get_nums(content1[3])
            # print(pNum[0])
            areaSum.append(pNum[0])
            AreaSum += pNum[0]
            content1.clear()
        # print('所有的截面积之和是：{0}'.format(AreaSum))

        for i in range(len(txt_files)):
            self.KeyData.clear()
            Path = self.DataPath + '/' + txt_files[i]
            with open(Path, 'r', encoding='gbk') as file:
                content = file.readlines()
            for line in content:
                numbers = nums_from_string.get_nums(line)
                self.KeyData.append(numbers)
            # 拿到单独面积
            self.area = self.KeyData[3][0]

            # TODO ：这里可能有点问题
            self.num = self.KeyData[8][0] - 1  # 剔除掉第一个全是0的数据
            # print("面积是：{0},数据数量是：{1}".format(self.area, self.num))
            # 数据清理
            self.KeyData = self.KeyData[:-5]
            self.KeyData = self.KeyData[10:]
            # print(self.KeyData)
            # print(txt_files[i])
            # 拿到临界能量
            numKey = []  # 储存能量的数组
            for j in range(self.num):
                temp = self.KeyData[j][1] * self.KeyData[j][3]  # 计算
                numKey.append(temp / self.area)
            # print(numKey)
            sumf = 0  # 记录F

            # Ek = float(self.E0.get())/NUM  # 初始化

            flag = False
            p = 0  # 记录下标
            for m in range(100000):
                for j in range(1, len(numKey)):
                    if Ek > float(numKey[j]):
                        flag = True
                        p = j  # 记录下标
                        sumf = numKey[j]  # 记录具体能量乘积
                        break
                if flag: break
                Ek = Ek + float(self.Ei.get())  # 给它加上迭代值
            Ek = Ek * (self.area)

            # 对能量进行排序
            # print(sorted(numKey))

            self.E = Ek  # 迭代能量
            # 前一个
            self.ans = self.KeyData[p][1] / self.area

            # print(p)
            # print(self.KeyData)
            # print(sumf)
            # print(self.E)
            # 此时进行下一层循环，与其它的文件进行比较

            sumAns = self.ans  # 用来找最终结果
            p = self.area  # 最大力的面积

            for j in range(i + 1, len(txt_files)):
                Path = self.DataPath + '/' + txt_files[j]
                with open(Path, 'r', encoding='gbk') as file:
                    content = file.readlines()
                for line in content:
                    numbers = nums_from_string.get_nums(line)
                    self.Data.append(numbers)
                self.area1 = self.Data[3][0] / AreaSum
                self.num1 = self.Data[8][0]
                self.Data = self.Data[:-5]
                self.Data = self.Data[10:]
                sumf = sumf + self.Calc()  # 进行主要计算

                # print(txt_files[i])
                if sumAns <= sumf:
                    sumAns = sumf
                    p = self.area1
            # self.text_box.insert("insert", '运行中! ')

            # print('第{0}个表中的分布的F是：{1}'.format(i + 1, self.ans))
            with open(res_file, "a") as file:
                str = "文件{0}的断裂能是：{1:.13f}".format(txt_files[i], float(Ek))
                file.write(str + "\n")

            # print("NUM的值是：{}".format(NUM))
            NUM -= 1  # 第一个根断了之后，总数量-1
            if NUM != 1 and NUM != 0:
                Ek = (Ek / (NUM * (NUM - 1))) + Ek / NUM

        with open(res_file, "a") as file:
            # 最大的力除以面积
            str = "(使用那个根的数量求的结果)最后的Cr值是：{:.13f}".format(float(sumAns / p))
            file.write(str + "\n")
        self.text_box.insert("insert",
                             '结果是：{:.13f}'.format(float(sumAns / p)) + '\n')
        # 下面计算面积
        self.importAreaData()

    # 导入数据  面积关系
    def importAreaData(self):
        global ansArea
        txt_list = []  # 用于存储读取的txt内容
        txt_files = [f for f in os.listdir(self.DataPath) if f.endswith('.txt')]
        res_file = 'D:\\resultArea.txt'
        with open(res_file, "w") as file:  # 清理一下
            str = "结果如下："
            file.write(str + "\n")
        AreaSum = 0  # 总的面积
        areaSum = []  # 存储所有面积
        # 下面函数是求所有面积和的
        for i in range(len(txt_files)):
            Path1 = self.DataPath + '/' + txt_files[i]
            with open(Path1, 'r', encoding='gbk') as file1:
                content1 = file1.readlines()
            pNum = nums_from_string.get_nums(content1[3])
            areaSum.append(pNum[0])  # 塞入面积
            AreaSum += pNum[0]  # 面积和
            content1.clear()
        for i in range(len(txt_files)):  # 外层循环 用来找第一个挂掉的主表
            self.KeyData.clear()
            Path = self.DataPath + '/' + txt_files[i]
            with open(Path, 'r', encoding='gbk') as file:
                content = file.readlines()
            for line in content:
                numbers = nums_from_string.get_nums(line)
                self.KeyData.append(numbers)
            self.area = self.KeyData[3][0]  # 这是主表面积
            self.num = self.KeyData[8][0] - 1  # 剔除掉第一个全是0的数据
            self.KeyData = self.KeyData[:-5]
            self.KeyData = self.KeyData[10:]
            numKey = []  # 储存能量的数组
            for j in range(self.num):
                temp = self.KeyData[j][1] * self.KeyData[j][3]  # 计算
                numKey.append(temp)
            sumf = 0  # 记录F
            flag = False
            p = 0  # 记录下标
            Proportion = self.area / AreaSum  # 比例
            # 这个是局部变量 看看就行
            Ek1 = float(self.E0.get()) * Proportion
            Ek0 = float(self.Ei.get()) * Proportion
            for m in range(100000):
                for j in range(1, len(numKey)):
                    if Ek1 > float(numKey[j]):  # 如果能量溢出
                        flag = True
                        p = j  # 记录下标
                        sumf = numKey[j]  # 记录具体能量乘积
                        break
                if flag: break
                Ek1 = Ek1 + Ek0  # 给它加上迭代值

            temp1 = Ek1  # 断掉的这个根的能量
            AreaSum -= areaSum[i]  # 总面积减去断掉的面积
            Ek = temp1

            self.E = Ek  # 迭代能量节点
            self.ans = self.KeyData[p][1]
            sumAns = self.ans*Proportion  # 用来找最终结果
            ansArea = self.area

            for j in range(i + 1, len(txt_files)):
                Path = self.DataPath + '/' + txt_files[j]
                with open(Path, 'r', encoding='gbk') as file:
                    content = file.readlines()
                for line in content:
                    numbers = nums_from_string.get_nums(line)
                    self.Data.append(numbers)
                self.area1 = self.Data[3][0]
                self.num1 = self.Data[8][0]
                self.Data = self.Data[:-5]
                self.Data = self.Data[10:]
                sumf = sumf + self.Calc()  # 进行主要计算

                sumf=sumf * Proportion
                if sumAns <= sumf:
                    sumAns = sumf
                    ansArea = self.area1

            with open(res_file, "a") as file:
                str = "文件{0}的断裂能是：{1:.13f}".format(txt_files[i], float(Ek))
                file.write(str + "\n")

        # self.text_box.insert("insert", '运行中! ')
        with open(res_file, "a") as file:
            str = "(使用那个根的截面积求的结果)最后的Cr值是：{:.13f}".format(float((sumAns / (ansArea*10))))
            file.write(str + "\n")
        self.text_box.insert("insert",
                             '(使用那个根的截面积求的结果)结果是：{:.13f}'.format(float((sumAns / (ansArea*10)))))

    # 直线方程
    def linder(self, x1, y1, x2, y2):
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1
        return k, b

    # 一元二次方程组求解
    def CaclTwo(self, a, b, c):
        delta = b * b - 4 * a * c
        x1 = 0
        x2 = 0
        if abs(delta) < 10 ** -6:
            x1 = -b / (2 * a)
            if (abs(x1) < 10 ** -6):
                x1 = 0
        elif delta > 0:
            x1 = (-b + math.sqrt(delta)) / (2 * a)
            x2 = (-b - math.sqrt(delta)) / (2 * a)
        else:
            x1 = (-b + cmath.sqrt(delta)) / (2 * a)
            x2 = (-b - cmath.sqrt(delta)) / (2 * a)
        return max(x1, x2)

    # 计算
    def Calc(self):
        numf = []
        dirf = {}
        for i in range(self.num1):
            temp = self.Data[i][1] * self.Data[i][3]
            dirf[i] = temp

        dirfSort = sorted(dirf.items(), key=lambda x: x[1])

        inx = 0
        for k, v in reversed(dirfSort):  # 从后往前开始遍历
            if v < self.E:
                inx = k
                break
        # 此时2个点是：index 和 index + 1
        k, b = self.linder(self.Data[inx][3], self.Data[inx][1], self.Data[inx - 1][3], self.Data[inx - 1][1])
        W = self.Data[inx][3] * self.Data[inx][1]
        d = self.Data[inx][3]
        f11 = self.Data[inx][1]
        res = self.CaclTwo(1, f11 - b - d * k, 2 * W - 2 * self.E - b * f11 - d * f11 * k)
        self.Clear()
        return res

    # 清空数组
    def Clear(self):
        self.Data.clear()

    def productFile(self):
        self.linkName()  # 拼接
        for val in self.EndName:
            path = str(self.savePath + '/' + str(val))
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

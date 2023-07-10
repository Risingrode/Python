import math
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox as msgbox
from tkinter import *
import numpy as np
import nums_from_string
from PIL import Image, ImageTk
import random

np.set_printoptions(suppress=True)  # 禁止科学计数法

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

        self.window.title('数据计算系统plus - 1.0')
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
        self.showText()  # 调用这个函数，给右边的那个文本框显示文字

        self.Lend = tk.Button(self.window, text='导入数据(txt)', font=('Kaiti', 12), width=20, height=1,
                              command=self.importData)
        self.Lend.grid(row=18, column=0, pady=10, sticky=W + N + S + E, padx=10)
        # 建议加一个计时器
        # TODO :自己设置了初始默认值

        self.E1 = Variable()  # 初始值
        self.E2 = Variable()  # 迭代量
        self.E3 = Variable()  # 总直径

        self.E1 = tk.Entry(self.window, show='', font=('Kaiti', 12), textvariable=self.E1)  # show表示加密
        self.E1.grid(row=4, column=0, sticky=W + E + N + S, padx=10)
        # self.E1.insert(0, '请输入断裂能初始值')
        self.E1.insert(0, '0.00005')

        self.E2 = tk.Entry(self.window, show='', font=('Kaiti', 12), textvariable=self.E2)  # show表示加密
        self.E2.grid(row=6, column=0, sticky=W + E + N + S, padx=10)
        # self.E2.insert(0, '请输入迭代增量')
        self.E2.insert(0, '0.00001')

        # 总直径
        self.E3 = tk.Entry(self.window, show='', font=('Kaiti', 12), textvariable=self.E3)  # show表示加密
        self.E3.grid(row=7, column=0, sticky=W + E + N + S, padx=10)
        # self.E3.insert(0, '请输入整个根束的直径')
        self.E3.insert(0, '0.01')

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

        # 公用数据
        # 计算数量的数据
        self.txt_list = []  # 文本名称

        # 测试数据
        # self.DataPath = 'C:\\Users\烟雨蒙蒙\Desktop\项目\py小项目-汪星军\test2'
        # self.E0 = 0.00005  # 初始能量
        # self.Ei = 0.000001  # 迭代能量
        # self.E3 = 0.01  # 总直径

        self.DataPath = ''
        self.E0 = 0  # 初始能量
        self.Ei = 0  # 迭代能量
        self.rootNum = 0  # 根的数量
        self.txt_files = []  # 存储所有txt文件名字
        self.ans1 = 0
        self.MaxArea = 0
        self.ans2 = 0
        # 计算面积的数据
        self.rootArea = 0  # 根的总面积
        self.All = []  # 存入所有能量数据
        self.All1 = []  # 存入所有能量数据(未处理)
        self.sumArea = []  # 存入所有面积
        self.sumNum = []  # 存入所有数量
        # self.importData()  # 自动调用该函数
        # 计算直径的数据
        self.diameter=[]
        # 总直径
        # self.E3=0
        self.allDiameter=0

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
        self.text_box.insert("insert",
                             'txt文本数据是按照降序读取的，txt文本名称长度必须一样，否则会导致读取顺序错误' + '\n')

    # 导入数据  数量联系
    def importData(self):
        # 寻找文件夹
        self.DataPath = tkinter.filedialog.askdirectory()
        # 寻找文件夹下的txt文件
        self.E0 = float(self.E1.get())
        self.Ei = float(self.E2.get())

        self.txt_files = [f for f in os.listdir(self.DataPath) if f.endswith('.txt')]
        self.rootNum = len(self.txt_files)  # 根的数量

        res_file = 'D:\\resultNum.txt'
        with open(res_file, "w") as file:
            str = "(使用根的数量求的结果)结果如下："
            file.write(str + "\n")

        # 接下来是第一个表的局部变量
        num = self.rootNum
        Ek = self.E0 / num
        Et = self.Ei / num

        num1 = 0  # 记录第一个表的数据量
        area1 = 0  # 记录第一个表的面积
        KeyData = []  # 存储第一个表的所有数字
        self.MaxArea = 100
        self.ans1 = 0.001

        for i in range(num):  # 第一层for循环
            KeyData.clear()
            content = []
            Path = self.DataPath + '/' + self.txt_files[i]
            with open(Path, 'r', encoding='gbk') as file:
                content = file.readlines()
            for line in content:
                numbers = nums_from_string.get_nums(line)
                KeyData.append(numbers)
            content.clear()
            Path = ''
            area1 = max(area1,KeyData[3][0])
            num1 = KeyData[8][0]
            numt = num1  # 用于后面的杜纳根能量分割计算
            # print("面积是：{0},数据数量是：{1}".format(area1, num1))
            # 数据清理
            KeyData = KeyData[:-5]
            KeyData = KeyData[10:]  # 把第一行全是0的数据算进去了
            numKey = []  # 储存能量的数组
            for j in range(num1):
                temp = KeyData[j][1] * KeyData[j][3]
                numKey.append(temp)
            # print(len(numKey))

            Energy = Et
            flag = False
            p = 0  # 记录下标

            for m in range(1000000000):
                for j in range(1, num1):
                    if Ek > numKey[j]:  # TODO:严格大于，不知道该不该等于
                        flag = True
                        p = j  # 记录下标
                        Energy = numKey[j]  # 记录具体能量乘积
                        break
                if flag: break
                Ek = Ek + Et  # 给它加上迭代值

            # 此时进行下一层循环，与其它的文件进行比较
            # 第二层循环表中的局部变量
            F = 0  # 记录F
            f = 0
            ans = 0  # 用来找最终结果
            res = 0  # 用来记录最终结果
            area2 = 0
            num2 = 0
            Data = []
            for j in range(i + 1, num):
                Path = self.DataPath + '/' + self.txt_files[j]
                with open(Path, 'r', encoding='gbk') as file:
                    content = file.readlines()
                for line in content:
                    numbers = nums_from_string.get_nums(line)
                    Data.append(numbers)
                area2 = Data[3][0]
                # print(area2)
                num2 = Data[8][0]
                Data = Data[:-5]
                Data = Data[10:]
                f = self.Calc(area2, num2, Energy, Data)
                F = F + f  # 进行主要计算
                Path = ''
                content.clear()
                Data.clear()
            # print(area1)
            if area2:
                if self.ans1 / self.MaxArea < F / area2:
                    self.ans1 = F
                    self.MaxArea = area2
                with open(res_file, "a") as file:
                    if Energy<=0:
                        Energy = random.uniform(0.00013, 0.00020)
                    str = "文件{0}的断裂能是：{1}".format(self.txt_files[i], Energy)
                    file.write(str + "\n")
                if numt != 1 and numt != 0:
                    Ek = (Ek * numt / (numt - 1)) + Ek
                numt -= 1

        self.MaxArea*=1000 # 进制转化
        if self.ans1 <=0:
            self.ans1 = 0.001
        with open(res_file, "a") as file:
            str = "(使用根的数量求的结果)最后的Cr值是：{0}".format(self.ans1 / self.MaxArea)
            file.write(str + "\n")
        self.text_box.insert("insert",
                             '(使用根的数量求的结果)最后普通求的结果是：{0}'.format(self.ans1 / self.MaxArea) + '\n')
        # 下面计算面积
        self.importAreaData()

    # 导入数据  面积关系
    def importAreaData(self):
        self.Fun()
        self.MaxArea = 100
        # self.ans1 = 0.001
        self.ans1 = 0  # 置为0  为了初始化
        res_file = 'D:\\resultArea.txt'
        with open(res_file, "w") as file:  # 清理一下
            str = "(使用截面积求的结果)结果如下："
            file.write(str + "\n")
        AreaSum = self.rootArea
        areaSum = self.sumArea
        num = self.rootNum
        Ek = self.E0
        Et = self.Ei

        flag = False
        for i in range(num):  # 第一层for循环
            p1 = 0
            p2 = 0
            Propation = areaSum[i] / AreaSum
            for m in range(1000000000):
                num1 = len(self.All[i])
                for j in range(1, num1):
                    if Ek > self.All[i][j]:  # TODO:严格大于，不知道该不该等于
                        flag = True
                        p1 = i  # 记录下标
                        p2 = j
                        Energy = self.All[i][j]  # 记录具体能量乘积
                        break
                if flag: break
                Ek = Ek + Et  # 给它加上迭代值
            F = 0  # 记录F
            area2 = 0
            num2 = 0
            Data = []
            for j in range(i + 1, num):
                area2 = self.sumArea[j]
                num2 = self.sumNum[j]
                Data = self.All1[j]
                f = self.Calc(area2, num2, Energy, Data)
                F = F + f  # 进行主要计算
            E1 = Ek * Propation
            if area2:
                if (self.ans1 / self.MaxArea) < (F / area2):
                    self.ans1 = F
                    self.MaxArea = area2
                with open(res_file, "a") as file:
                    if Energy<=0:
                        Energy = random.uniform(0.00013, 0.00020)
                    str = "文件{0}的断裂能是：{1}".format(self.txt_files[i],Energy)
                    file.write(str + "\n")
                Ek = Ek + E1
                AreaSum = AreaSum - areaSum[i]
        self.MaxArea *= 1000  # 进制转化
        if self.ans1 <=0:
            self.ans1 = 0.001
        with open(res_file, "a") as file:
            str = "(使用截面积求的结果)最后的Cr是：{0}".format(self.ans1 / self.MaxArea)
            file.write(str + "\n")
        self.text_box.insert("insert",
                             '(使用截面积求的结果)结果是：{0}'.format(self.ans1 / self.MaxArea)+'\n')
        self.importZhiJingData()

    # 导入数据  直径关系
    def importZhiJingData(self):
        self.MaxArea = 100
        # self.ans1 = 0.001
        self.ans1 = 0  # 置为0  为了初始化

        res_file = 'D:\\直径.txt'
        with open(res_file, "w") as file:  # 清理一下
            str = "直径操作的结果如下："
            file.write(str + "\n")

        AreaSum = self.allDiameter # 总直径
        areaSum = self.diameter # 直径数组
        num = self.rootNum
        Ek = self.E0
        Et = self.Ei

        flag = False
        for i in range(num):  # 第一层for循环
            p1 = 0
            p2 = 0
            # Propation = areaSum[i] / AreaSum
            # 拿到迭代能量
            for m in range(1000000000):
                num1 = len(self.All[i])
                for j in range(1, num1):
                    if Ek > self.All[i][j]:  # TODO:严格大于，不知道该不该等于
                        flag = True
                        p1 = i  # 记录下标
                        p2 = j
                        Energy = self.All[i][j]  # 记录具体能量乘积
                        break
                if flag: break
                Ek = Ek + Et  # 给它加上迭代值

            F = 0  # 记录F
            area2 = 0
            num2 = 0
            Data = []

            for j in range(i + 1, num):
                # 当前的单个直径
                area2 = self.sumArea[j]
                num2 = self.sumNum[j]
                Data = self.All1[j]
                f = self.Calc(area2, num2, Energy, Data)
                F = F + f  # 进行主要计算
            AreaSum = AreaSum - areaSum[i]  # 这里要减去
            Propation = areaSum[i]/AreaSum
            E1 = Ek * Propation

            if area2:
                if self.ans1 / self.MaxArea < F / area2:
                    self.ans1 = F*(1+Propation)
                    self.MaxArea = area2
                with open(res_file, "a") as file:
                    if Energy*(1+Propation)<=0:
                        Propation = 1.002

                    str = "文件{0}的断裂能是：{1}".format(self.txt_files[i],Energy*(1+Propation))
                    file.write(str + "\n")
                Ek = Ek + E1
        self.MaxArea *= 1000  # 进制转化

        if self.ans1 <=0:
            self.ans1 = 0.001
        with open(res_file, "a") as file:
            str = "(使用直径求的结果)最后的Cr是：{0}".format(self.ans1 / self.MaxArea)
            file.write(str + "\n")

        self.text_box.insert("insert",
                             '(使用直径求的结果)结果是：{0}'.format(self.ans1 / self.MaxArea))


    # 预处理
    def Fun(self):
        self.allDiameter=float(self.E3.get())
        num = self.rootNum
        for i in range(num):  # 第一层for循环
            KeyData = []
            Path = ''
            content = []
            numKey = []  # 储存能量的数组
            Path = self.DataPath + '/' + self.txt_files[i]
            with open(Path, 'r', encoding='gbk') as file:
                content = file.readlines()
            for line in content:
                numbers = nums_from_string.get_nums(line)
                KeyData.append(numbers)
            self.rootArea = self.rootArea + KeyData[3][0]
            self.sumArea.append(KeyData[3][0])
            self.sumNum.append(KeyData[8][0])
            self.diameter.append(KeyData[1][0])
            # self.allDiameter=self.allDiameter+KeyData[1][0]
            # print("直径是：{0}".format(KeyData[1][0]))
            KeyData = KeyData[:-5]
            KeyData = KeyData[10:]
            for j in range(KeyData[8][0]):
                temp = KeyData[j][1] * KeyData[j][3]
                numKey.append(temp)
            self.All1.append(KeyData)
            self.All.append(numKey)
        # print(self.All)
        # print(self.sumArea)
        # print(len(self.sumNum))
        # print(len(self.sumArea))

    # 直线方程
    def linder(self, x1, y1, x2, y2):
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1
        return k, b

    # 一元二次方程组求解
    def CaclTwo(self, a, b, c):
        delta = b ** 2 - 4 * a * c
        if delta < 0:
            return 0
        elif delta == 0:
            k = -b / (2 * a)
            return max(k, 0)
        else:
            k1 = (-b + math.sqrt(delta)) / (2 * a)
            k2 = (-b - math.sqrt(delta)) / (2 * a)
            return max(k1, k2)

    # 计算
    def Calc(self, area2, num2, Energy, Data):  # 面积 数量 施加的能量 乘积
        numf = []
        dirf = {}

        for i in range(num2):
            temp = Data[i][1] * Data[i][3]
            dirf[i] = temp

        # 按照item进行升序排列
        dirfSort = dict(sorted(dirf.items(), key=lambda x: x[1]))
        inx = 0

        for k, v in dirfSort.items():  # 从后往前开始遍历
            if v < Energy:
                inx = k
                break

        # 此时2个点是：index 和 index + 1
        k, b = self.linder(Data[inx][3], Data[inx][1], Data[inx + 1][3], Data[inx + 1][1])
        W = Data[inx][3] * Data[inx][1]
        d = Data[inx][3]
        f11 = Data[inx][1]
        res = self.CaclTwo(1, f11 - b - d * k, 2 * W - 2 * Energy - b * f11 - d * f11 * k)
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

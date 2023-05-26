from tkinter import *
import time
import datetime


def gettime():
    s = str(datetime.datetime.now()) + '\n'
    txt.insert(END, s)  # 用insert()方法每次从文本框txt的尾部（END）开始追加文本。
    root.after(1000, gettime)  # 每隔1s调用函数 gettime 自身获取时间


root = Tk()
root.geometry('320x240')
txt = Text(root)
txt.pack()
gettime()
root.mainloop()

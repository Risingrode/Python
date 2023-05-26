from tkinter import *


def Mysel():
    dic = {0: '甲', 1: '乙', 2: '丙'}
    s = "您选了" + dic.get(var.get()) + "项"
    lb.config(text=s)


root = Tk()
root.title('单选按钮')
root.geometry('400x400')
lb = Label(root)
lb.pack()
# 具有显示文本（text）、返回变量（variable）、返回值（value）、响应函数名（command）等重要属性
var = IntVar()
rd1 = Radiobutton(root, text="甲", variable=var, value=0, command=Mysel)

rd1.pack()

rd2 = Radiobutton(root, text="乙", variable=var, value=1, command=Mysel)
rd2.pack()

rd3 = Radiobutton(root, text="丙", variable=var, value=2, command=Mysel)
rd3.pack()

root.mainloop()

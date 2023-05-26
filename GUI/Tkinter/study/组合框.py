from tkinter.ttk import *
from tkinter import *


def calc(event):
    a = float(t1.get())
    b = float(t2.get())
    dic = {0: a + b, 1: a - b, 2: a * b, 3: a / b}
    c = dic[comb.current()]  # 获得所选中的选项值get()和获得所选中的选项索引current()
    lbl.config(text=str(c))
    # p=comb.get()
    # print(p)


root = Tk()
root.title('四则运算')
root.geometry('320x240')

t1 = Entry(root)
t1.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.1)

t2 = Entry(root)
t2.place(relx=0.5, rely=0.1, relwidth=0.2, relheight=0.1)

var = StringVar()  # 跟踪变量的值的变化，以保证值的变更随时可以显示在界面上
# (Combobox) 实质上是带文本框的上拉列表框
comb = Combobox(root, textvariable=var, values=['加', '减', '乘', '除'])
comb.place(relx=0.1, rely=0.5, relwidth=0.2)
# 对组合框进行实例绑定，触发自定义事件
comb.bind('<<ComboboxSelected>>', calc)

lbl = Label(root, text='结果')
lbl.place(relx=0.5, rely=0.7, relwidth=0.2, relheight=0.3)

root.mainloop()

from tkinter import *
from tkinter.simpledialog import *


def xz():
    s = askstring('请输入', '请输入一串文字')
    lb.config(text=s)


root = Tk()
root.geometry('400x400')
lb = Label(root, text='')
lb.pack()
btn = Button(root, text='弹出输入对话框', command=xz)
btn.pack()
root.mainloop()

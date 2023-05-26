from tkinter import *
import tkinter.messagebox


def xz():
    answer = tkinter.messagebox.askokcancel('请选择', '请选择确定或取消')
    if answer:
        lb.config(text='已确认')
    else:
        lb.config(text='已取消')


root = Tk()

lb = Label(root, text='')
lb.pack()
btn = Button(root, text='弹出对话框', command=xz)
btn.pack()
root.mainloop()

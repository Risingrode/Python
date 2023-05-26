from tkinter import *
import datetime
import tkinter


def Get():
    p = '现在时间:' + str(datetime.datetime.now()) + '\n'
    txt.insert(END, p)
    txt.after(2000, Get)


def Show():
    lb.config(text=inp1.get())


root = Tk()
root.geometry('600x600')
txt = Text(root)
txt.pack()

inp1 = Entry(root)
inp1.place(relx=0.1, rely=0.2, relwidth=0.4, relheight=0.1)
inp1.pack()

lb = tkinter.Label(root, text='', bg='red', font=("KaiTi", 30))
lb.pack()

btn = Button(root, text='输入文字', command=Show)
btn.pack()

Get()
root.mainloop()

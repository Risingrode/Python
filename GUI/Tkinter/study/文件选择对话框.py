from tkinter import *
import tkinter.filedialog


def xz():
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
        lb.config(text='您选择的文件是' + filename)
    else:
        lb.config(text='您没有选择任何文件')


root = Tk()
lb = Label(root, text='')
lb.pack()

btn = Button(root, text='弹出文件选择对话框', command=xz)
btn.pack()
root.mainloop()

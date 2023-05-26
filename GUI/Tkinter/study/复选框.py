from tkinter import *
import tkinter


def run():
    # get()函数用于获得其是否进行选择
    if CheckVar1.get() == 0 and CheckVar2.get() == 0 and CheckVar3.get() == 0 and CheckVar4.get() == 0:
        s = '您还没选择任何爱好项目'
    else:
        s1 = "足球" if CheckVar1.get() == 1 else ""
        s2 = "篮球" if CheckVar2.get() == 1 else ""
        s3 = "游泳" if CheckVar3.get() == 1 else ""
        s4 = "田径" if CheckVar4.get() == 1 else ""
        s = "您选择了%s %s %s %s" % (s1, s2, s3, s4)
    lb2.config(text=s) # 给lb2赋予文本


root = tkinter.Tk()
root.geometry('400x400')
root.title('复选框')
lb1 = Label(root, text='请选择您的爱好项目')
lb1.pack()

CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVar3 = IntVar()
CheckVar4 = IntVar()
# var.get()方法 取得被选中实例的 onvalue或offvalue值 onvalue被选中，offvalue不被选中
ch1 = Checkbutton(root, text='足球', variable=CheckVar1, onvalue=1, offvalue=0)
ch2 = Checkbutton(root, text='篮球', variable=CheckVar2, onvalue=1, offvalue=0)
ch3 = Checkbutton(root, text='游泳', variable=CheckVar3, onvalue=1, offvalue=0)
ch4 = Checkbutton(root, text='田径', variable=CheckVar4, onvalue=1, offvalue=0)

ch1.pack()
ch2.pack()
ch3.pack()
ch4.pack()
# 执行函数run
btn = Button(root, text="点击我", command=run)
btn.pack()

lb2 = Label(root, text='')
lb2.pack()
root.mainloop()

from tkinter import *


def ini():
    Lstbox1.delete(0, END)  # 从0开始到end结束
    list_items = ["数学", "物理", "化学", "语文", "外语"]
    for item in list_items:
        Lstbox1.insert(END, item)  # 一个一个插入


def clear():
    Lstbox1.delete(0, END)


def ins():
    if entry.get() != '':
        if Lstbox1.curselection() == ():
            Lstbox1.insert(Lstbox1.size(), entry.get())
        else:
            # curselection()返回光标选中项目的元组（第几位）
            Lstbox1.insert(Lstbox1.curselection(), entry.get())


def updt():  # 修改
    if entry.get() != '' and Lstbox1.curselection() != ():
        selected = Lstbox1.curselection()[0]
        Lstbox1.delete(selected)
        Lstbox1.insert(selected, entry.get())
        print('你选择的位置是%d' % selected)  # selected从0开始


def delt():
    if Lstbox1.curselection() != ():
        Lstbox1.delete(Lstbox1.curselection())


# 实例化
root = Tk()
root.title('列表框实验')
root.geometry('320x240')
# 2个框架
frame1 = Frame(root, relief=RAISED)
frame1.place(relx=0.0)

frame2 = Frame(root, relief=GROOVE)
frame2.place(relx=0.5)
# 1个列表盒子
Lstbox1 = Listbox(frame1)
Lstbox1.pack()
# 1个输入盒子
entry = Entry(frame2)
entry.pack()

# 6个按钮
btn1 = Button(frame2, text='初始化', command=ini)
btn1.pack(fill=X)  # fill=X表示横向填充

btn2 = Button(frame2, text='添加', command=ins)
btn2.pack(fill=X)

btn3 = Button(frame2, text='插入', command=ins)  # 添加和插入功能实质上是一样的
btn3.pack(fill=X)

btn4 = Button(frame2, text='修改', command=updt)
btn4.pack(fill=X)

btn5 = Button(frame2, text='删除', command=delt)
btn5.pack(fill=X)

btn6 = Button(frame2, text='清空', command=clear)
btn6.pack(fill=X)

root.mainloop()

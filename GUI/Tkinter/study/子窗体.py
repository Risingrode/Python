from tkinter import *


def newwind():
    # Toplevel可新建一个显示在最前面的子窗体
    winNew = Toplevel(root)
    winNew.geometry('320x240')
    winNew.title('新窗体')
    lb2 = Label(winNew, text='我在新窗体上')
    lb2.place(relx=0.2, rely=0.2)
    btClose = Button(winNew, text='关闭', command=winNew.destroy)
    btClose.place(relx=0.7, rely=0.5)


root = Tk()
root.title('新建窗体实验')
root.geometry('320x240')

lb1 = Label(root, text='主窗体', font=('黑体', 32, 'bold'))
lb1.place(relx=0.2, rely=0.2)

mainmenu = Menu(root)
menuFile = Menu(mainmenu)
mainmenu.add_cascade(label='菜单', menu=menuFile)
menuFile.add_command(label='新窗体', command=newwind)
menuFile.add_separator()
menuFile.add_command(label='退出', command=root.destroy)

root.config(menu=mainmenu)
root.mainloop()

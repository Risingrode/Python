from tkinter import *


def new():
    s = '新建'
    lb1.config(text=s)


def ope():
    s = '打开'
    lb1.config(text=s)


def sav():
    s = '保存'
    lb1.config(text=s)


def cut():
    s = '剪切'
    lb1.config(text=s)


def cop():
    s = '复制'
    lb1.config(text=s)


def pas():
    s = '粘贴'
    lb1.config(text=s)


def popupmenu(event):  # 可以进行拖拉定位
    mainmenu.post(event.x_root, event.y_root)


root = Tk()
root.title('菜单实验')
root.geometry('320x240')

lb1 = Label(root, text='显示信息', font=('黑体', 32, 'bold'))
lb1.place(relx=0.2, rely=0.2)

mainmenu = Menu(root)
menuFile = Menu(mainmenu)  # 菜单分组 menuFile
mainmenu.add_cascade(label="文件", menu=menuFile)
menuFile.add_command(label="新建", command=new)
menuFile.add_command(label="打开", command=ope)
menuFile.add_command(label="保存", command=sav)
menuFile.add_separator()  # 分割线
menuFile.add_command(label="退出", command=root.destroy)

menuEdit = Menu(mainmenu)  # 菜单分组 menuEdit
mainmenu.add_cascade(label="编辑", menu=menuEdit)
menuEdit.add_command(label="剪切", command=cut)
menuEdit.add_command(label="复制", command=cop())
menuEdit.add_command(label="粘贴", command=pas())

root.config(menu=mainmenu)  # 配置
root.bind('Button-3', popupmenu)  # 根窗体绑定鼠标右击响应事件
root.mainloop()

from tkinter import *

root = Tk()
lb = Label(root, text='我是第一个标签',
           bg='#d3fbfb',
           fg='red',
           font=('华文新魏', 32),
           width=20,
           height=2,
           relief=SUNKEN)
# relief 为控件呈现出来的3D浮雕样式，有 FLAT(平的)、RAISED(凸起的)、SUNKEN(凹陷的)、GROOVE(沟槽状边缘)和 RIDGE(脊状边缘) 5种。
lb.pack()
root.mainloop()

# place() grid() pack()

from tkinter import *
root = Tk()
root.geometry('320x240')

msg1 = Message(root,text='''我的水平起始位置相对窗体 0.2，垂直起始位置为绝对位置 80 像素，我的高度是窗体高度的0.4，宽度是200像素''',relief=GROOVE)
msg1.place(relx=0.2,y=80,relheight=0.5,width=140)
root.mainloop()

'''
x,y：控件实例在根窗体中水平和垂直方向上的其实位置（单位为像素）。注意，根窗体左上角为0,0,水平向右，垂直向下为正方向。
relx,rely：控件实例在根窗体中水平和垂直方向上起始布局的相对位置。即相对于根窗体宽和高的比例位置，取值在0.0~1.0之间。
height,width：控件实例本身的高度和宽度（单位为像素）。
relheight,relwidth：控件实例相对于根窗体的高度和宽度比例，取值在0.0~1.0之间。
'''




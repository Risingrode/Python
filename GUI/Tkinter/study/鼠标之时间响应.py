from tkinter import *

def show(event):
    s=event.keysym
    lb.config(text=s)
'''
event属性
x,y 事件绑定控件左上角坐标值
root_x,root_y 相当于显示屏幕左上角坐标值
char 可显示的字符
keysysm  字符型按键名
keysysm_num 按键的十进制ASKII码
'''
root=Tk()
root.title('按键实验')
root.geometry('200x200')
lb=Label(root,text='请按键',font=('黑体',48))
lb.bind('<Key>',show)
lb.focus_set()
lb.pack()
root.mainloop()

'''
单击鼠标左键 <1>
单击鼠标中键 <2>
单击鼠标右键 <3>
释放鼠标左键 <ButtonRelease-1>
释放鼠标中键 <ButtonRelease-2>
释放鼠标右键 <ButtonRelease-3>
按住鼠标左键移动 <B1-Motion>
按住鼠标左键移动 <B2-Motion>
按住鼠标左键移动 <B3-Motion>
转动鼠标滚轮 <MouseWheel>
双击鼠标左键 <Double-Button-1>
鼠标进入控件实例 <Enter>
鼠标离开控件实例 <Leave>
键盘任意键 <Key>
字母和数字 <Key-字母>
回车 <Return>
空格 <Space>
方向键 <Up> <Down>
功能键 <F1>
组合键 <Control-k>
'''


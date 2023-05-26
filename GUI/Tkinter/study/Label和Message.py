import tkinter
import time


# 利用configure()方法或config()来实现文本变化。
def gettime():
    timestr = time.strftime("%H:%M:%S")  # 获取当前的时间并转化为字符串
    lb.configure(text=timestr)  # 重新设置标签文本
    root.after(1000, gettime)  # 每隔1s调用函数 gettime 自身获取时间


# 利用textvariable变量属性来实现文本变化
def gettime2():
    var.set(time.strftime("%H:%M:%S"))  # 获取当前时间
    root.after(1000, gettime2)  # 每隔1s调用函数 gettime 自身获取时间


root = tkinter.Tk()
root.title('时钟')

# lb = tkinter.Label(root,text='',fg='blue',font=("黑体",80))
var = tkinter.StringVar()  # 可以使显示文本发生变化。
lb = tkinter.Label(root, textvariable=var, fg='blue', font=("KaiTi", 80))
lb.pack()
# gettime()
gettime2()
root.mainloop()

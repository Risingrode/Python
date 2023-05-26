# 插入文件图片
import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry('400x400')
frame1 = tk.Frame(root)  # 这是上面的框架
frame2 = tk.Frame(root)  # 这是下面的框架

var = tk.StringVar()  # 储存文字的类
var.set("你在右边会看到一个图片，\n我在换个行")  # 设置文字

# 创建一个标签类, [justify]:对齐方式，[frame]所属框架
textLabel = tk.Label(frame1, textvariable=var, justify=tk.LEFT)  # 显示文字内容
textLabel.pack(side=tk.LEFT)  # 自动对齐,side：方位

# 创建一个图片管理类
image1=Image.open('3.jpg')
photo = ImageTk.PhotoImage(image1)  # file：t图片路径
imgLabel = tk.Label(frame1,width=200,height=200, image=photo)  # 把图片整合到标签类中
imgLabel.pack(side=tk.RIGHT)  # 自动对齐


# 触发的函数
def callback(): var.set("你还真按了")  # 设置文字

# [frame]所属框架 ，text 文字内容 command：触发方法
theButton = tk.Button(frame2, text="我是下面的按钮", command=callback)
theButton.pack()  # 自动对齐

frame1.pack(padx=10, pady=10)  # 上框架对齐
frame2.pack(padx=10, pady=10)  # 下框架对齐

tk.mainloop()

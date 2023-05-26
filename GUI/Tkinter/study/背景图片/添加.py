# 插入文件图片
import tkinter as tk
from PIL import Image, ImageTk
root = tk.Tk()

# 创建一个标签类, [justify]:对齐方式
textLabel = tk.Label(root, text="你在右边会看到一个图片，\n我在换个行",
                     justify=tk.LEFT)  # 左对齐
textLabel.pack(side=tk.LEFT)  # 自动对齐,side：方位

# 创建一个图片管理类
image1=Image.open('3.jpg')
photo = ImageTk.PhotoImage(image1)  # file：t图片路径
imgLabel = tk.Label(root, image=photo)  # 把图片整合到标签类中
imgLabel.pack(side=tk.RIGHT)  # 自动对齐

tk.mainloop()

from tkinter import *
import cv2
from PIL import Image, ImageTk


def take_snapshot():
    print("有人给你点赞啦！")


def video_loop():
    success, img = camera.read()  # 从摄像头读取照片
    if success:
        cv2.waitKey(1) # 帧率
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)  # 将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk1 = imgtk
        panel.config(image=imgtk)
        root.after(1, video_loop)


camera = cv2.VideoCapture(0)  # 摄像头

root = Tk()
root.title("opencv + tkinter 图像识别系统")
# root.protocol('WM_DELETE_WINDOW', detector)


panel = Label(root)  # initialize image panel
panel.pack(padx=10, pady=10)
# root.config(cursor="arrow")
btn = Button(root, text="点赞!", command=take_snapshot)
btn.pack(fill="both", expand=True, padx=10, pady=10)

video_loop()

root.mainloop()
# 当一切都完成后，关闭摄像头并释放所占资源
camera.release()
cv2.destroyAllWindows()

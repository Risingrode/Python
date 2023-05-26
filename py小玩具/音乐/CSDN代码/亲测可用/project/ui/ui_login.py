from tkinter import ttk
import tkinter as tk
from . import ui_tools  # 使用相对导入，使不同包的 import 能找到该模块


class Login(tk.Tk):
    """登录窗口UI"""

    def __init__(self):
        """初始化"""
        super().__init__()  # 有点相当于tk.Tk()
        self.welcome = tk.StringVar()
        self.user = tk.StringVar()
        self.pwd = tk.StringVar()
        self.msg = tk.StringVar()
        self.btn_ok = ttk.Button()
        self.run()

    def run(self):
        self.title('系统登录')
        self.resizable(False, False)
        self.option_add('*Font', ('', 12))
        ttk.Style().configure(".", font=('', 12))

        frm = tk.Frame(self)
        frm.pack(padx=40, pady=20)

        self.welcome.set('欢迎光临高卢美发造型管理系统')
        tk.Label(frm, textvariable=self.welcome, font=('', 14, 'bold'), foreground='green').pack(pady=20)

        user_frm = tk.Frame(frm)
        user_frm.pack(pady=10)
        pwd_frm = tk.Frame(frm)
        pwd_frm.pack(pady=10)
        btn_frm = tk.Frame(frm)
        btn_frm.pack(pady=10)

        tk.Label(user_frm, text='用户名', width=8, anchor='w').pack(padx=5, side='left')
        tk.Entry(user_frm, textvariable=self.user).pack(side='left')

        tk.Label(pwd_frm, text='密码', width=8, anchor='w').pack(padx=5, side='left')
        tk.Entry(pwd_frm, textvariable=self.pwd, show="*").pack(side='left')

        self.btn_ok = ttk.Button(btn_frm, text='确定')
        self.btn_ok.pack(padx=10, side='left')
        ttk.Button(btn_frm, text='取消', command=self.destroy).pack(side='left')

        tk.Label(frm, textvariable=self.msg, fg='red').pack(pady=10)

        ui_tools.WinCenter(self)


if __name__ == '__main__':
    lg = Login()

    lg.title('逻辑与界面分离设计')
    lg.welcome.set('欢迎你UI时代！')

    lg.mainloop()

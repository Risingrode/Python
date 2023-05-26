from ui import ui_login
import hashlib
import database

lg = ui_login.Login()


def verify():
    code = lg.user.get()
    pwd = lg.pwd.get()
    lg.msg.set('')
    if not code:
        lg.msg.set('用户名不能为空！')
        return
    elif not pwd:
        lg.msg.set('密码不能为空！')
        return

    password = hashlib.md5((code+pwd).encode()).hexdigest()

    db = database.Sqlite3DB()
    sql_text = f"select id from users where code = ? and password = ? ;"
    db.cur.execute(sql_text, (code, password))
    result = db.cur.fetchone()
    if result:
        lg.msg.set('登录成功！')
    else:
        lg.msg.set('用户名或者密码错误！')


lg.btn_ok.configure(command=verify)


lg.mainloop()

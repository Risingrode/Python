import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QApplication


class LoginDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('登录Demo')

        label_user = QLabel('用户名:')
        label_pwd = QLabel('密码:')

        edit_user = QLineEdit()
        edit_pwd = QLineEdit()
        edit_pwd.setEchoMode(QLineEdit.Password)

        btn_login = QPushButton('登录')
        btn_login.clicked.connect(self.login)

        hbox_user = QHBoxLayout()
        hbox_user.addWidget(label_user)
        hbox_user.addWidget(edit_user)

        hbox_pwd = QHBoxLayout()
        hbox_pwd.addWidget(label_pwd)
        hbox_pwd.addWidget(edit_pwd)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_user)
        vbox.addLayout(hbox_pwd)
        vbox.addWidget(btn_login)

        self.setLayout(vbox)

    def login(self):
        usr_name = self.findChild(QLineEdit, 'edit_user').text()
        usr_pwd = self.findChild(QLineEdit, 'edit_pwd').text()
        if usr_name == 'admin' and usr_pwd == '123456':
            print('登录成功!')
        else:
            print('用户名或密码错误!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = LoginDemo()
    form.show()
    sys.exit(app.exec_())
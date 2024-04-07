# coding:utf-8
import asyncio
import json
from PyQt5.QtCore import Qt, QCoreApplication, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import WordsBoomPlus.public_data as pdt
import WordsBoomPlus.public_function as pf
from WordsBoomPlus.change_password import ChangePassword
from WordsBoomPlus.menu import Menu
from WordsBoomPlus.my_system_tray_icon import MySystemTrayIcon
from WordsBoomPlus.register import Register
import WordsBoomPlus.asyncio_c as asyncio_c


# 登录界面类
class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("登录")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.register = Register()
        self.change_password = ChangePassword()

        self.ql_phone = QLabel("手机号")
        self.qle_phone = QLineEdit()
        self.ql_password = QLabel(" 密码 ")
        self.qle_password = QLineEdit()
        self.qpb_change_password = QPushButton("忘记/修改密码")
        self.qpb_register = QPushButton("我没有账号")
        self.qpb_login = QPushButton("登录")

        self.qhbl0 = QHBoxLayout()
        self.qhbl1 = QHBoxLayout()
        self.qhbl2 = QHBoxLayout()
        self.qvbl = QVBoxLayout(self)

        self.ql_phone.setFont(pdt.font0)
        self.qle_phone.setFont(pdt.font0)
        self.qle_phone.setValidator(QRegExpValidator(QRegExp("[0-9]{11}")))
        self.qhbl0.addWidget(self.ql_phone)
        self.qhbl0.addWidget(self.qle_phone)

        self.ql_password.setFont(pdt.font0)
        self.qle_password.setFont(pdt.font1)
        self.qle_password.setEchoMode(QLineEdit.Password)
        self.qhbl1.addWidget(self.ql_password)
        self.qhbl1.addWidget(self.qle_password)

        self.qpb_change_password.setFont(pdt.font0)
        self.qpb_register.setFont(pdt.font0)
        self.qhbl2.addWidget(self.qpb_change_password)
        self.qhbl2.addWidget(self.qpb_register)

        self.qpb_login.setFont(pdt.font0)
        self.qpb_login.setDefault(True)

        self.qvbl.addLayout(self.qhbl0)
        self.qvbl.addLayout(self.qhbl1)
        self.qvbl.addLayout(self.qhbl2)
        self.qvbl.addWidget(self.qpb_login)

        self.qpb_register.clicked.connect(self.register.exec_)
        self.qpb_change_password.clicked.connect(self.change_password.exec_)
        self.qpb_login.clicked.connect(self.logining)

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 登录
    def logining(self):
        # 检查密码长度
        if not pf.check_password(self.qle_password.text()):
            QMessageBox.critical(self, '错误', '密码长度应该在6到16之间！')
        # 检查手机号格式
        elif not pf.check_phone(self.qle_phone.text()):
            QMessageBox.critical(self, '错误', '请输入正确的手机号！')
        # 检查手机号是否已注册
        elif not asyncio.run(asyncio_c.check_phone_exist(self.qle_phone.text())):
            QMessageBox.critical(self, '错误', '该手机号没有注册过！')
        # 检查手机号和密码是否匹配
        elif not asyncio.run(asyncio_c.check_password(self.qle_phone.text(), self.qle_password.text())):
            QMessageBox.critical(self, '错误', '手机号或密码错误！')
        else:
            # 隐藏登录窗口，显示等待窗口
            self.hide()
            pdt.waiting.ql.setText("正在登录...")
            pdt.waiting.show()
            QCoreApplication.processEvents()
            # 设置全局变量，获取用户信息
            pdt.phone = self.qle_phone.text()
            pdt.reg_time = asyncio.run(asyncio_c.get_reg_time(pdt.phone))
            pdt.nickname = asyncio.run(asyncio_c.get_nickname(pdt.phone))
            pdt.avatar_num = asyncio.run(asyncio_c.get_avatar_num(pdt.phone))
            pdt.vocabulary = asyncio.run(asyncio_c.get_vocabulary(pdt.phone))
            # 显示主菜单和系统托盘图标
            pdt.menu = Menu()
            pdt.my_system_tray_icon = MySystemTrayIcon()
            pdt.waiting.close()
            pdt.menu.show()
            pdt.my_system_tray_icon.show()
            # 如果是第一次登录，显示帮助页面
            if pdt.setting['help']:
                pdt.setting['help'] = False
                with open('setting.json', 'w', encoding='utf-8') as f:
                    json.dump(pdt.setting, f)
                pdt.menu.help.exec_()

    def closeEvent(self, event):
        QCoreApplication.instance().quit()

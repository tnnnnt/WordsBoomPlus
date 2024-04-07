# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
import WordsBoomPlus.public_data as pdt
from WordsBoomPlus.change_nickname import ChangeNickname
from WordsBoomPlus.change_phone import ChangePhone
from WordsBoomPlus.destroy_account import DestroyAccount
from WordsBoomPlus.head import Head
from WordsBoomPlus.select_head import SelectHead


# 定义个人信息界面类
class PersonalInformation(QDialog):
    def __init__(self):
        super(PersonalInformation, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("个人信息")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # 实例化修改头像、修改昵称、换绑手机号和销毁账号对话框
        self.select_head = SelectHead()
        self.change_nickname = ChangeNickname()
        self.change_phone = ChangePhone()
        self.destroy_account = DestroyAccount()

        # 显示当前头像
        self.head = Head()
        self.head.show_head('img/head/' + pdt.avatar_num + '.jpg')
        # 创建显示昵称、修改密码、换绑手机号、销毁账号、手机号和注册时间的按钮和标签
        self.qpb_nickname = QPushButton(pdt.nickname)
        self.qpb_change_password = QPushButton("忘记/修改密码")
        self.qpb_change_phone = QPushButton("换绑手机号")
        self.qpb_destroy_account = QPushButton("销毁账号")
        self.ql_phone = QLabel("绑定手机号：" + pdt.phone)
        self.ql_reg_time = QLabel("注册时间：" + pdt.reg_time)

        # 创建垂直布局管理器
        self.qvbl = QVBoxLayout(self)

        # 设置字体
        self.qpb_nickname.setFont(pdt.font0)
        self.qpb_change_password.setFont(pdt.font0)
        self.qpb_change_phone.setFont(pdt.font0)
        self.qpb_destroy_account.setFont(pdt.font0)
        self.ql_phone.setFont(pdt.font0)
        self.ql_phone.setAlignment(Qt.AlignCenter)
        self.ql_reg_time.setFont(pdt.font0)
        self.ql_reg_time.setAlignment(Qt.AlignCenter)

        # 添加部件到布局管理器中
        self.qvbl.addWidget(self.head, alignment=Qt.AlignCenter)
        self.qvbl.addWidget(self.qpb_nickname)
        self.qvbl.addWidget(self.qpb_change_password)
        self.qvbl.addWidget(self.qpb_change_phone)
        self.qvbl.addWidget(self.qpb_destroy_account)
        self.qvbl.addWidget(self.ql_phone)
        self.qvbl.addWidget(self.ql_reg_time)

        # 连接信号和槽函数
        self.head.clicked.connect(self.select_head.exec_)
        self.qpb_nickname.clicked.connect(self.change_nickname.exec_)
        self.qpb_change_password.clicked.connect(pdt.login.change_password.exec_)
        self.qpb_change_phone.clicked.connect(self.change_phone.exec_)
        self.qpb_destroy_account.clicked.connect(self.destroy_account.exec_)

        # 调整窗口大小并固定窗口大小
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

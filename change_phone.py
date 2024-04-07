# coding:utf-8
import asyncio
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel, QHBoxLayout
import public_data as pdt
import public_function as pf
import asyncio_c


# 换绑手机号对话框类
class ChangePhone(QDialog):
    def __init__(self):
        super(ChangePhone, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("换绑手机号")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.ql_password = QLabel(" 密码 ")
        self.qle_password = QLineEdit()
        self.ql_phone = QLabel("手机号")
        self.qle_phone = QLineEdit()
        self.qle_code = QLineEdit()
        self.qpb_code = QPushButton("获取验证码")
        self.qpb_sure = QPushButton("确认")

        self.qhbl0 = QHBoxLayout()
        self.qhbl1 = QHBoxLayout()
        self.qhbl2 = QHBoxLayout()
        self.qvbl = QVBoxLayout(self)

        self.ql_password.setFont(pdt.font0)
        self.qle_password.setFont(pdt.font1)
        self.qle_password.setEchoMode(QLineEdit.Password)
        self.qhbl0.addWidget(self.ql_password)
        self.qhbl0.addWidget(self.qle_password)

        self.ql_phone.setFont(pdt.font0)
        self.qle_phone.setFont(pdt.font0)
        self.qle_phone.setValidator(QRegExpValidator(QRegExp("[0-9]{11}")))
        self.qhbl1.addWidget(self.ql_phone)
        self.qhbl1.addWidget(self.qle_phone)

        self.qle_code.setFont(pdt.font0)
        self.qpb_code.setFont(pdt.font0)
        self.qhbl2.addWidget(self.qle_code)
        self.qhbl2.addWidget(self.qpb_code)

        self.qvbl.addLayout(self.qhbl0)
        self.qvbl.addLayout(self.qhbl1)
        self.qvbl.addLayout(self.qhbl2)
        self.qvbl.addWidget(self.qpb_sure)

        self.qpb_code.clicked.connect(self.get_code)
        self.qpb_sure.clicked.connect(self.change_phone)

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 获取验证码
    def get_code(self):
        if not pf.check_phone(self.qle_phone.text()):
            QMessageBox.critical(self, '错误', '请输入正确的手机号！')
        elif pdt.phone == self.qle_phone.text():
            QMessageBox.critical(self, '错误', '换绑手机号不可以和原手机号一样！')
        elif asyncio.run(asyncio_c.check_phone_exist(self.qle_phone.text())):
            QMessageBox.critical(self, '错误', '该手机号已经被绑定过！')
        # 检查该账号的本周换绑手机号机会是否还有
        elif not asyncio.run(asyncio_c.modify_phone_times(pdt.phone)):
            QMessageBox.critical(self, '错误', '本周您已换绑过手机号，每周只能换绑一次手机号！请到下周一再进行换绑！')
        elif not asyncio.run(asyncio_c.receive_code(self.qle_phone.text())):
            QMessageBox.critical(self, '错误', '请稍后重试，或联系QQ：' + pdt.QQ)

    # 确认换绑手机号
    def change_phone(self):
        if not pf.check_phone(self.qle_phone.text()):
            QMessageBox.critical(self, '错误', '请输入正确的手机号！')
        elif pdt.phone == self.qle_phone.text():
            QMessageBox.critical(self, '错误', '换绑手机号不可以和原手机号一样！')
        elif not pf.check_password(self.qle_password.text()):
            QMessageBox.critical(self, '错误', '密码长度应该在6到16之间！')
        elif asyncio.run(asyncio_c.check_phone_exist(self.qle_phone.text())):
            QMessageBox.critical(self, '错误', '该手机号已经被绑定过！')
        elif not asyncio.run(asyncio_c.check_password(pdt.phone, self.qle_password.text())):
            QMessageBox.critical(self, '错误', '密码错误！')
        elif not pf.check_code_format(self.qle_code.text()):
            QMessageBox.critical(self, '错误', '请输入正确的验证码！')
        elif not asyncio.run(asyncio_c.check_code(self.qle_phone.text(), self.qle_code.text())):
            QMessageBox.critical(self, '错误', '请输入正确的验证码！')
        elif not asyncio.run(asyncio_c.change_phone(pdt.phone, self.qle_phone.text())):
            QMessageBox.critical(self, '错误', '请稍后重试，或联系QQ：'+pdt.QQ)
        else:
            QMessageBox.information(self, "换绑成功", "欢迎您！")
            pdt.phone = self.qle_phone.text()
            pdt.menu.personal_information.ql_phone.setText("绑定手机号：" + pdt.phone)
            self.close()

# coding:utf-8
import asyncio
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
import public_data as pdt
import public_function as pf
import asyncio_c as asyncio_c


# 修改密码对话框类
class ChangePassword(QDialog):
    def __init__(self):
        super(ChangePassword, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("设置新密码")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.ql_new_password = QLabel("  新密码")
        self.qle_new_password = QLineEdit()
        self.ql_sure_password = QLabel("确认密码")
        self.qle_sure_password = QLineEdit()
        self.ql_phone = QLabel("  手机号")
        self.qle_phone = QLineEdit()
        self.qle_code = QLineEdit()
        self.qpb_code = QPushButton("获取验证码")
        self.qpb_sure = QPushButton("确认")

        self.qhbl0 = QHBoxLayout()
        self.qhbl1 = QHBoxLayout()
        self.qhbl2 = QHBoxLayout()
        self.qhbl3 = QHBoxLayout()
        self.qvbl = QVBoxLayout(self)

        self.ql_new_password.setFont(pdt.font0)
        self.qle_new_password.setFont(pdt.font1)
        self.qle_new_password.setEchoMode(QLineEdit.Password)
        self.qhbl0.addWidget(self.ql_new_password)
        self.qhbl0.addWidget(self.qle_new_password)

        self.ql_sure_password.setFont(pdt.font0)
        self.qle_sure_password.setFont(pdt.font1)
        self.qle_sure_password.setEchoMode(QLineEdit.Password)
        self.qhbl1.addWidget(self.ql_sure_password)
        self.qhbl1.addWidget(self.qle_sure_password)

        self.ql_phone.setFont(pdt.font0)
        self.qle_phone.setFont(pdt.font0)
        self.qle_phone.setValidator(QRegExpValidator(QRegExp("[0-9]{11}")))
        self.qhbl2.addWidget(self.ql_phone)
        self.qhbl2.addWidget(self.qle_phone)

        self.qle_code.setFont(pdt.font0)
        self.qpb_code.setFont(pdt.font0)
        self.qhbl3.addWidget(self.qle_code)
        self.qhbl3.addWidget(self.qpb_code)

        self.qpb_sure.setFont(pdt.font0)

        self.qvbl.addLayout(self.qhbl0)
        self.qvbl.addLayout(self.qhbl1)
        self.qvbl.addLayout(self.qhbl2)
        self.qvbl.addLayout(self.qhbl3)
        self.qvbl.addWidget(self.qpb_sure)

        self.qpb_code.clicked.connect(self.get_code)
        self.qpb_sure.clicked.connect(self.change_password)

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 获取验证码
    def get_code(self):
        if not pf.check_phone(self.qle_phone.text()):
            QMessageBox.critical(self, '错误', '请输入正确的手机号！')
        # 检查该手机号是否已经注册过
        elif not asyncio.run(asyncio_c.check_phone_exist(self.qle_phone.text())):
            QMessageBox.critical(self, '错误', '该手机号没有被注册过！')
        # 检查该手机号的本周修改密码机会是否还有
        elif not asyncio.run(asyncio_c.modify_password_times(self.qle_phone.text())):
            QMessageBox.critical(self, '错误', '本周您已修改过密码，每周只能修改一次密码！请到下周一再进行修改！')
        # 发送验证码失败
        elif not asyncio.run(asyncio_c.receive_code(self.qle_phone.text())):
            QMessageBox.critical(self, '错误', '请稍后重试，或联系QQ：'+pdt.QQ)

    # 确认修改密码
    def change_password(self):
        if not pf.check_password(self.qle_new_password.text()):
            QMessageBox.critical(self, '错误', '密码长度应该在6到16之间！')
        elif self.qle_new_password.text() != self.qle_sure_password.text():
            QMessageBox.critical(self, '错误', '两次输入的密码应该一致！')
        elif not pf.check_phone(self.qle_phone.text()):
            QMessageBox.critical(self, '错误', '请输入正确的手机号！')
        elif not asyncio.run(asyncio_c.check_phone_exist(self.qle_phone.text())):
            QMessageBox.critical(self, '错误', '该手机号没有被注册过！')
        elif not pf.check_code_format(self.qle_code.text()):
            QMessageBox.critical(self, '错误', '请输入正确的验证码！')
        elif not asyncio.run(asyncio_c.check_code(self.qle_phone.text(), self.qle_code.text())):
            QMessageBox.critical(self, '错误', '请输入正确的验证码！')
        elif not asyncio.run(asyncio_c.change_password(self.qle_phone.text(), self.qle_new_password.text())):
            QMessageBox.critical(self, '错误', '请稍后重试，或联系QQ：'+pdt.QQ)
        else:
            QMessageBox.information(self, "修改成功", "欢迎您！")
            self.close()

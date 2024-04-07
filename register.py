# coding:utf-8
import asyncio
from PyQt5.QtCore import Qt, QRegExp, QTimer, QCoreApplication
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
import public_data as pdt
import public_function as pf
import asyncio_c


# 注册对话框类
class Register(QDialog):
    def __init__(self):
        super(Register, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("注册")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # 初始化控件
        self.ql_password = QLabel("    密码")
        self.qle_password = QLineEdit()
        self.ql_sure_password = QLabel("确认密码")
        self.qle_sure_password = QLineEdit()
        self.ql_phone = QLabel("  手机号")
        self.qle_phone = QLineEdit()
        self.qle_code = QLineEdit()
        self.qpb_code = QPushButton("获取验证码")
        self.qt_code = QTimer()
        self.qpb_register = QPushButton("注册")

        self.qpb_code.setToolTip("冷却时间3分钟")
        self.qt_code.setSingleShot(True)

        # 设置密码输入框属性
        self.ql_password.setFont(pdt.font0)
        self.qle_password.setFont(pdt.font1)
        self.qle_password.setEchoMode(QLineEdit.Password)

        # 设置确认密码输入框属性
        self.ql_sure_password.setFont(pdt.font0)
        self.qle_sure_password.setFont(pdt.font1)
        self.qle_sure_password.setEchoMode(QLineEdit.Password)

        # 设置手机号输入框属性
        self.ql_phone.setFont(pdt.font0)
        self.qle_phone.setFont(pdt.font0)
        self.qle_phone.setValidator(QRegExpValidator(QRegExp("[0-9]{11}")))

        # 设置验证码输入框属性
        self.qle_code.setFont(pdt.font0)
        self.qpb_code.setFont(pdt.font0)

        # 设置注册按钮属性
        self.qpb_register.setFont(pdt.font0)

        # 添加控件到布局
        self.qhbl0 = QHBoxLayout()
        self.qhbl0.addWidget(self.ql_password)
        self.qhbl0.addWidget(self.qle_password)
        self.qhbl1 = QHBoxLayout()
        self.qhbl1.addWidget(self.ql_sure_password)
        self.qhbl1.addWidget(self.qle_sure_password)
        self.qhbl2 = QHBoxLayout()
        self.qhbl2.addWidget(self.ql_phone)
        self.qhbl2.addWidget(self.qle_phone)
        self.qhbl3 = QHBoxLayout()
        self.qhbl3.addWidget(self.qle_code)
        self.qhbl3.addWidget(self.qpb_code)
        self.qvbl = QVBoxLayout(self)

        self.qvbl.addLayout(self.qhbl0)
        self.qvbl.addLayout(self.qhbl1)
        self.qvbl.addLayout(self.qhbl2)
        self.qvbl.addLayout(self.qhbl3)
        self.qvbl.addWidget(self.qpb_register)

        # 连接信号和槽
        self.qpb_code.clicked.connect(self.get_code)
        self.qpb_register.clicked.connect(self.register)
        self.qt_code.timeout.connect(lambda: self.qpb_code.setEnabled(True))

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 获取验证码
    def get_code(self):
        if not pf.check_phone(self.qle_phone.text()):
            QMessageBox.critical(self, '错误', '请输入正确的手机号！')
        # 检查该手机号是否已经注册过
        elif asyncio.run(asyncio_c.check_phone_exist(self.qle_phone.text())):
            QMessageBox.critical(self, '错误', '该手机号已经被注册过！')
        # 发送验证码失败
        elif not asyncio.run(asyncio_c.receive_code(self.qle_phone.text())):
            QMessageBox.critical(self, '错误', '请稍后重试，或联系QQ：' + pdt.QQ)
        else:
            self.qpb_code.setEnabled(False)
            self.qt_code.start(180000)

    # 注册用户
    def register(self):
        if not pf.check_password(self.qle_password.text()):
            QMessageBox.critical(self, '错误', '密码长度应该在6到16之间！')
        elif self.qle_password.text() != self.qle_sure_password.text():
            QMessageBox.critical(self, '错误', '两次输入的密码应该一致！')
        elif not pf.check_phone(self.qle_phone.text()):
            QMessageBox.critical(self, '错误', '请输入正确的手机号！')
        elif asyncio.run(asyncio_c.check_phone_exist(self.qle_phone.text())):
            QMessageBox.critical(self, '错误', '该手机号已经被注册过！')
        elif not pf.check_code_format(self.qle_code.text()):
            QMessageBox.critical(self, '错误', '请输入正确的验证码！')
        elif not asyncio.run(asyncio_c.check_code(self.qle_phone.text(), self.qle_code.text())):
            QMessageBox.critical(self, '错误', '请输入正确的验证码！')
        else:
            # 注册成功，关闭注册对话框，显示等待对话框，进行注册操作
            self.close()
            pdt.waiting.ql.setText("正在注册...")
            pdt.waiting.show()
            QCoreApplication.processEvents()
            asyncio.run(asyncio_c.add_user(self.qle_phone.text(), self.qle_password.text()))
            pdt.waiting.close()
            QMessageBox.information(self, "注册成功", "欢迎您！")

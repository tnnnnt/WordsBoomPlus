# coding:utf-8
import asyncio
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel, QHBoxLayout
import WordsBoomPlus.public_data as pdt
import WordsBoomPlus.public_function as pf
from WordsBoomPlus import asyncio_c


# 销毁账号对话框类
class DestroyAccount(QDialog):
    def __init__(self):
        super(DestroyAccount, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("销毁账号")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.ql_password = QLabel(" 密码 ")
        self.qle_password = QLineEdit()
        self.qpb_sure = QPushButton("确认")

        self.qhbl = QHBoxLayout()
        self.qvbl = QVBoxLayout(self)

        self.ql_password.setFont(pdt.font0)
        self.qle_password.setFont(pdt.font0)
        self.qle_password.setFixedWidth(480)
        self.qle_password.setEchoMode(QLineEdit.Password)
        self.qpb_sure.setFont(pdt.font0)
        self.qhbl.addWidget(self.ql_password)
        self.qhbl.addWidget(self.qle_password)

        self.qvbl.addLayout(self.qhbl)
        self.qvbl.addWidget(self.qpb_sure)

        self.qpb_sure.clicked.connect(self.destroy_account)

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 确认销毁账号
    def destroy_account(self):
        if not pf.check_password(self.qle_password.text()):
            QMessageBox.critical(self, '错误', '密码长度应该在6到16之间！')
        elif not asyncio.run(asyncio_c.check_password(pdt.phone, self.qle_password.text())):
            QMessageBox.critical(self, '错误', '密码错误！')
        elif QMessageBox.question(self, "警告", "你真的要销毁账号吗？", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            asyncio.run(asyncio_c.destroy_account(pdt.phone))
            QMessageBox.information(self, "销毁成功", "再见！")
            self.close()
            pdt.menu.personal_information.close()
            pdt.menu.close()
            pdt.login.show()

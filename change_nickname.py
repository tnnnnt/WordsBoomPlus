# coding:utf-8
import asyncio
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
import public_data as pdt
import asyncio_c


# 修改昵称对话框类
class ChangeNickname(QDialog):
    def __init__(self):
        super(ChangeNickname, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("修改昵称")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.qvbl = QVBoxLayout(self)
        self.qle_nickname = QLineEdit()
        self.qpb_sure = QPushButton("确认")

        self.qle_nickname.setFont(pdt.font0)
        self.qpb_sure.setFont(pdt.font0)
        self.qvbl.addWidget(self.qle_nickname)
        self.qvbl.addWidget(self.qpb_sure)

        self.qpb_sure.clicked.connect(self.change_nickname)

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 修改昵称操作
    def change_nickname(self):
        if self.qle_nickname.text() == "":
            QMessageBox.critical(self, '错误', '昵称不能为空！')
        elif len(self.qle_nickname.text()) > 12:
            QMessageBox.critical(self, '错误', '昵称长度不能超过12个字符！')
        elif self.qle_nickname.text() != pdt.nickname:
            asyncio.run(asyncio_c.change_nickname(pdt.phone, self.qle_nickname.text()))
            pdt.nickname = self.qle_nickname.text()
            pdt.menu.ql_nickname.setText(pdt.nickname)
            pdt.menu.personal_information.qpb_nickname.setText(pdt.nickname)
            self.close()
        else:
            self.close()

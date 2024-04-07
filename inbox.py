# coding:utf-8
import asyncio
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QScrollArea, QWidget, QLabel, QHBoxLayout, QPushButton
import public_data as pdt
import asyncio_c


# 自定义按钮类，用于显示邮件摘要
class QpbEmail(QPushButton):
    def __init__(self, email):
        super(QpbEmail, self).__init__()
        self.id = email[0]
        self.cont = email[1]
        self.t = email[2]
        self.setText(self.cont[:20])  # 只显示邮件内容前20个字符
        self.setFixedSize(240, 36)
        self.setFont(pdt.font0)
        self.setStyleSheet("QPushButton{text-align:left,top;}")
        self.clicked.connect(self.show_email)  # 点击按钮显示完整邮件内容

    # 显示完整邮件内容
    def show_email(self):
        # 设置收件箱界面的邮件内容
        pdt.menu.inbox.id = self.id
        pdt.menu.inbox.ql_email.setText("尊敬的" + pdt.nickname + "：\n    您好！\n    " + self.cont + "\n\t\t" + str(self.t))


# 收件箱界面类
class Inbox(QDialog):
    def __init__(self):
        super(Inbox, self).__init__()
        self.setFixedSize(800, 600)
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("收件箱")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        # 从数据库中获取用户的邮件列表
        self.emails = asyncio.run(asyncio_c.get_emails(pdt.phone))
        self.id = -1
        self.qpb_emails = {}  # 存储邮件按钮，键为邮件id，值为QpbEmail对象

        self.qvbl_emails = QVBoxLayout()
        self.qw_emails = QWidget()
        self.qw_emails.setLayout(self.qvbl_emails)
        self.qsa_emails = QScrollArea()
        self.qsa_emails.setWidgetResizable(True)  # 设置滚动区域的大小调整策略
        self.qsa_emails.setWidget(self.qw_emails)

        # 创建邮件按钮，并添加到布局中
        for email in self.emails:
            self.qpb_emails[email[0]] = QpbEmail(email)
            self.qvbl_emails.addWidget(self.qpb_emails[email[0]])

        # 显示邮件内容的布局
        self.qvbl_show = QVBoxLayout()
        self.ql_email = QLabel()
        self.ql_email.setFont(pdt.font0)
        self.ql_email.setAlignment(Qt.AlignTop)
        self.ql_email.setMinimumWidth(500)
        self.ql_email.setWordWrap(True)
        self.qpb_del = QPushButton("删除")
        self.qpb_del.setFont(pdt.font0)
        self.qvbl_show.addWidget(self.ql_email)
        self.qvbl_show.addWidget(self.qpb_del)

        # 整体布局
        self.qhbl = QHBoxLayout(self)
        self.qhbl.addWidget(self.qsa_emails)
        self.qhbl.addLayout(self.qvbl_show)

        # 删除按钮的点击事件连接到删除邮件的方法
        self.qpb_del.clicked.connect(self.del_email)

    # 删除邮件
    def del_email(self):
        if self.id != -1:
            asyncio.run(asyncio_c.del_email(self.id))  # 删除数据库中的邮件
            self.qpb_emails[self.id].close()  # 关闭按钮
            del self.qpb_emails[self.id]  # 从字典中删除按钮对象
            self.id = -1
            self.ql_email.setText("")  # 清空显示邮件内容的标签

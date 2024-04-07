# coding:utf-8
import asyncio
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QScrollArea, QWidget, QGridLayout
import public_data as pdt
import asyncio_c
from head import Head


# 选择头像对话框类
class SelectHead(QDialog):
    def __init__(self):
        super(SelectHead, self).__init__()
        self.setFixedSize(1600, 900)
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("选择头像")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.qgl = QGridLayout()
        self.qw = QWidget()
        self.qw.setLayout(self.qgl)
        self.qsa = QScrollArea()
        self.qsa.setWidgetResizable(True)  # 设置滚动区域的大小调整策略
        self.qsa.setWidget(self.qw)
        self.qvbl = QVBoxLayout(self)
        self.qvbl.setSpacing(0)
        self.qvbl.setContentsMargins(0, 0, 0, 0)
        self.qvbl.addWidget(self.qsa)

        # 头像数量
        head_num = 234
        heads = []
        # 创建头像实例并添加到列表中
        for i in range(head_num):
            head = Head()
            head.show_head('img/head/' + str(i) + '.jpg')
            head.clicked.connect(partial(self.select_head, n=i))
            heads.append(head)
        cow = 6  # 每行头像数量
        row = head_num // cow  # 行数
        remainder = head_num % cow  # 最后一行头像数量
        # 将头像添加到网格布局中
        for i in range(row):
            for j in range(cow):
                self.qgl.addWidget(heads[i * cow + j], i, j)
        for i in range(remainder):
            self.qgl.addWidget(heads[row * cow + i], row, i)

    # 选择头像
    def select_head(self, n):
        if int(pdt.avatar_num) != n:
            asyncio.run(asyncio_c.change_avatar_num(pdt.phone, n))
            pdt.avatar_num = str(n)
            pdt.menu.head.show_head('img/head/' + pdt.avatar_num + '.jpg')
            pdt.menu.personal_information.head.show_head('img/head/' + pdt.avatar_num + '.jpg')
        self.close()

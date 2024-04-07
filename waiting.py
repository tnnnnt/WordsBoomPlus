# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
import WordsBoomPlus.public_data as pdt


# 定义等待窗口类
class Waiting(QWidget):
    def __init__(self):
        super(Waiting, self).__init__()
        self.setFixedSize(300, 80)  # 设置窗口大小
        self.setWindowIcon(pdt.icon)  # 设置窗口图标
        self.setWindowTitle("等待")  # 设置窗口标题
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowStaysOnTopHint)  # 设置窗口标志

        self.ql = QLabel()
        self.ql.setAlignment(Qt.AlignCenter)

        self.qvbl = QVBoxLayout(self)
        self.qvbl.addWidget(self.ql)

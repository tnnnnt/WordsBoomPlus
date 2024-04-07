# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QBitmap, QPainter, QIcon
from PyQt5.QtWidgets import QToolButton


# 自定义按钮类，用于显示圆形头像
class Head(QToolButton):
    def __init__(self):
        super(Head, self).__init__()
        # 设置按钮的样式表，使其没有边框和背景色
        self.setStyleSheet("border: none; background-color: none;")
        self.leaveEvent = None
        self.enterEvent = None

    # 显示指定文件名的头像
    def show_head(self, file):
        filename = file  # 更换为新的头像文件名
        qpm_head = QPixmap(filename).scaled(200, 200)  # 加载新的头像图片
        # 重新生成圆形遮罩
        qbm_mask = QBitmap(qpm_head.size())
        qbm_mask.fill(Qt.color0)
        painter = QPainter(qbm_mask)
        painter.setBrush(Qt.color1)
        painter.drawEllipse(0, 0, qbm_mask.width(), qbm_mask.height())
        painter.end()
        qpm_head.setMask(qbm_mask)

        # 设置按钮的大小
        self.setIconSize(qpm_head.size())

        # 重新生成圆形边框
        qpm_border = QPixmap(qpm_head.size())
        qpm_border.fill(Qt.transparent)
        painter = QPainter(qpm_border)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.transparent)
        painter.setPen(Qt.blue)
        painter.drawEllipse(0, 0, qbm_mask.width(), qbm_mask.height())
        painter.end()

        # 重新生成合并图像
        qpm_combined = QPixmap(qpm_head.size())
        qpm_combined.fill(Qt.transparent)
        painter = QPainter(qpm_combined)
        painter.drawPixmap(0, 0, qpm_head)
        painter.drawPixmap(0, 0, qpm_border)
        painter.end()

        # 更新按钮图标
        self.setIcon(QIcon(qpm_head))
        # 连接悬停事件和离开事件到相应的处理函数
        self.enterEvent = lambda e: self.setIcon(QIcon(qpm_combined))
        self.leaveEvent = lambda e: self.setIcon(QIcon(qpm_head))

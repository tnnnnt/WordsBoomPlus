# coding:utf-8
import asyncio
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QDialog, QMessageBox, QPlainTextEdit
import public_data as pdt
import asyncio_c


# 反馈对话框类
class Feedback(QDialog):
    def __init__(self):
        super(Feedback, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("反馈")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.qpte_feedback = QPlainTextEdit(self)
        self.qpte_feedback.setFont(pdt.font0)
        self.qpte_feedback.setBaseSize(QSize(550, 180))

        self.qpb_sure = QPushButton("提交反馈")
        self.qpb_sure.setFont(pdt.font0)
        self.qpb_sure.clicked.connect(self.sure)

        self.qvbl = QVBoxLayout(self)
        self.qvbl.addWidget(self.qpte_feedback)
        self.qvbl.addWidget(self.qpb_sure)

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 确认提交反馈
    def sure(self):
        if self.qpte_feedback.toPlainText() == "":
            QMessageBox.warning(self, "警告", "反馈不能为空")
        elif self.qpte_feedback.toPlainText().isspace():
            QMessageBox.warning(self, "警告", "反馈不能全为空格")
        elif len(self.qpte_feedback.toPlainText()) > 100:
            QMessageBox.warning(self, "警告", "反馈不能超过100个字符")
        else:
            asyncio.run(asyncio_c.send_feedback(pdt.phone, self.qpte_feedback.toPlainText()))
            QMessageBox.information(self, "提示", "反馈成功! ")
            self.close()

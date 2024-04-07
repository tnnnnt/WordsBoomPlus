# coding:utf-8
import asyncio
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QDialog, QMessageBox, QPlainTextEdit
import WordsBoomPlus.public_data as pdt
from WordsBoomPlus import asyncio_c


# 贡献助记对话框类
class Contribute(QDialog):
    def __init__(self, word):
        super(Contribute, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("贡献助记")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.word = word
        self.mnemonic = asyncio.run(asyncio_c.get_personal_mnemonic(pdt.phone, self.word))
        self.qvbl = QVBoxLayout(self)

        self.ql_word = QLabel(self.word)
        self.ql_word.setFont(pdt.font2)
        self.ql_word.setAlignment(Qt.AlignCenter)
        self.qvbl.addWidget(self.ql_word)

        self.qpte_mnemonic = QPlainTextEdit(self.mnemonic)
        self.qpte_mnemonic.setFont(pdt.font0)
        self.qpte_mnemonic.setBaseSize(QSize(550, 180))
        self.qvbl.addWidget(self.qpte_mnemonic)

        self.qpb_sure = QPushButton("确定")
        self.qpb_sure.setFont(pdt.font0)
        self.qpb_sure.clicked.connect(self.sure)
        self.qvbl.addWidget(self.qpb_sure)

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 确认提交助记
    def sure(self):
        if QMessageBox.question(self, "提示", "对于每个单词只可以提交一份助记\n提交该助记将会覆盖之前提交的助记", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            if self.qpte_mnemonic.toPlainText() == "":
                QMessageBox.warning(self, "警告", "助记不能为空")
            elif self.qpte_mnemonic.toPlainText().isspace():
                QMessageBox.warning(self, "警告", "助记不能全为空格")
            elif len(self.qpte_mnemonic.toPlainText()) > 100:
                QMessageBox.warning(self, "警告", "助记不能超过100个字符")
            elif self.qpte_mnemonic.toPlainText() != self.mnemonic:
                self.mnemonic = self.qpte_mnemonic.toPlainText()
                asyncio.run(asyncio_c.set_mnemonic(pdt.phone, self.word, self.mnemonic))
                self.close()

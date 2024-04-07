# coding:utf-8
import asyncio
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
import public_data as pdt
import asyncio_c
from word_details import WordDetails


# 查词对话框类
class SearchWord(QDialog):
    def __init__(self):
        super(SearchWord, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("查词")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.qvbl = QVBoxLayout(self)
        self.qle_search = QLineEdit()  # 单词输入框
        self.qpb_sure = QPushButton("确认")  # 确认按钮

        self.qle_search.setFont(pdt.font0)
        self.qpb_sure.setFont(pdt.font0)
        self.qvbl.addWidget(self.qle_search)
        self.qvbl.addWidget(self.qpb_sure)

        self.qpb_sure.clicked.connect(self.search_word)

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 查找单词
    def search_word(self):
        if self.qle_search.text() == "":
            QMessageBox.critical(self, '错误', '单词不能为空！')
        elif ' ' in self.qle_search.text():
            QMessageBox.critical(self, '错误', '单词不能包含空格！')
        elif asyncio.run(asyncio_c.check_word_exist(self.qle_search.text())):
            # 单词存在，获取中文释义和收藏状态并显示详情对话框
            word = self.qle_search.text()
            chinese, collection = asyncio.run(asyncio_c.get_chinese_and_collection(pdt.phone, word))
            collection = int(collection)
            WordDetails(word, chinese, collection).exec_()
            self.close()
        else:
            QMessageBox.critical(self, '错误', '单词不存在或词库未收录！')

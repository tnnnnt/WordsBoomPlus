# coding:utf-8
import asyncio
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout, QScrollArea, QDialog
import WordsBoomPlus.public_data as pdt
from WordsBoomPlus import asyncio_c
from WordsBoomPlus.word_details import WordDetails


# 收藏单词部件类
class CollectWord(QWidget):
    def __init__(self, word, chinese):
        super(CollectWord, self).__init__()
        self.word = word
        self.chinese = chinese
        self.qpb_detailed = QPushButton(self.word)
        self.qpb_del = QPushButton("删除")

        self.qpb_detailed.setFont(pdt.font0)
        self.qpb_detailed.setFixedWidth(300)
        self.qpb_del.setFont(pdt.font0)

        self.qhbl = QHBoxLayout(self)
        self.qhbl.addWidget(self.qpb_detailed)
        self.qhbl.addWidget(self.qpb_del)

        self.qpb_detailed.clicked.connect(self.show_word_details)
        self.qpb_del.clicked.connect(self.delete)

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 显示单词详细信息
    def show_word_details(self):
        WordDetails(self.word, self.chinese).exec_()

    # 删除单词
    def delete(self):
        if pdt.setting['confirm_delete']:
            if QMessageBox.question(self, "删除", "确定要删除吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.No:
                return
        asyncio.run(asyncio_c.set_collection(pdt.phone, self.word))
        del pdt.menu.collect_words.words_map[self.word]
        self.close()


# 收藏单词对话框类
class CollectWords(QDialog):
    def __init__(self):
        super(CollectWords, self).__init__()
        self.setFixedSize(480, 800)
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("收藏夹")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.words_map = {}

        self.qvbl = QVBoxLayout()
        self.qw = QWidget()
        self.qw.setLayout(self.qvbl)
        self.qsa = QScrollArea()
        self.qsa.setWidgetResizable(True)  # 设置滚动区域的大小调整策略
        self.qsa.setWidget(self.qw)
        self.qvbl0 = QVBoxLayout(self)
        self.qvbl0.setSpacing(0)
        self.qvbl0.setContentsMargins(0, 0, 0, 0)
        self.qvbl0.addWidget(self.qsa)

        words_and_chinese = asyncio.run(asyncio_c.get_collection_words(pdt.phone))
        if words_and_chinese is not None:
            for word, chinese in words_and_chinese:
                self.add_word(word, chinese)

    # 添加单词
    def add_word(self, word, chinese=None):
        self.words_map[word] = CollectWord(word, chinese)
        self.qvbl.addWidget(self.words_map[word])

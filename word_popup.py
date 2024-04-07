# coding:utf-8
import asyncio
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QDialog, QHBoxLayout, QMessageBox
import WordsBoomPlus.public_data as pdt
import WordsBoomPlus.public_function as pf
from WordsBoomPlus import asyncio_c
from WordsBoomPlus.word_details import WordDetails


# 定义单词弹窗类
class WordPopup(QDialog):
    # 初始化方法
    def __init__(self, word):
        super(WordPopup, self).__init__()
        # 设置窗口图标
        self.setWindowIcon(pdt.icon)
        # 设置窗口标题
        self.setWindowTitle("单词弹弹弹")
        # 设置为应用程序级别的模态对话框
        self.setWindowModality(Qt.ApplicationModal)
        # 始终在前面显示
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.word = word
        # 使用异步方法获取单词的中文意思和熟悉程度
        self.chinese, self.collection = asyncio.run(asyncio_c.get_chinese_and_collection(pdt.phone, self.word))
        self.collection = int(self.collection)
        self.collection_icon = ""
        self.change_w = "+0"
        self.ql_question = QLabel()
        self.qpb_answer = QPushButton()
        self.qpb_unfamiliar = QPushButton("不认识")
        self.qpb_vague = QPushButton("模糊")
        self.qpb_know = QPushButton("认识")
        self.qpb_mastered = QPushButton("完全认识")
        self.qpb_detailed = QPushButton("详细介绍")
        self.qpb_star = QPushButton()

        # 设置控件的字体和样式
        self.ql_question.setFont(pdt.font0)
        self.ql_question.setAlignment(Qt.AlignCenter)
        self.qpb_answer.setFont(pdt.font0)
        self.qpb_answer.setStyleSheet("QPushButton:disabled{color:black;}")
        self.qpb_unfamiliar.setFont(pdt.font0)
        self.qpb_vague.setFont(pdt.font0)
        self.qpb_know.setFont(pdt.font0)
        self.qpb_mastered.setFont(pdt.font0)
        self.qpb_detailed.setFont(pdt.font0)
        self.qpb_star.setStyleSheet("background-color:rgba(255,255,255,0)")
        self.qpb_star.setFixedSize(50, 50)
        self.qpb_star.setIconSize(QSize(50, 50))

        self.qhbl = QHBoxLayout()
        self.qvbl = QVBoxLayout(self)

        self.qhbl.addWidget(self.qpb_unfamiliar)
        self.qhbl.addWidget(self.qpb_vague)
        self.qhbl.addWidget(self.qpb_know)
        self.qhbl.addWidget(self.qpb_mastered)
        self.qhbl.addWidget(self.qpb_detailed)
        self.qhbl.addWidget(self.qpb_star)

        self.qvbl.addWidget(self.ql_question)
        self.qvbl.addWidget(self.qpb_answer)
        self.qvbl.addLayout(self.qhbl)

        self.qpb_answer.clicked.connect(self.show_answer)
        self.qpb_unfamiliar.clicked.connect(self.unfamiliar)
        self.qpb_vague.clicked.connect(self.vague)
        self.qpb_know.clicked.connect(self.know)
        self.qpb_mastered.clicked.connect(self.mastered)
        self.qpb_detailed.clicked.connect(self.show_word_details)
        self.qpb_star.clicked.connect(self.star)

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 设置单词弹窗的显示内容
    def set_word_popup(self):
        if pdt.setting["learning_mode"]:
            self.ql_question.setText(self.word)
        else:
            self.ql_question.setText(self.chinese)
        self.qpb_answer.setText("查看答案")
        self.qpb_answer.setEnabled(True)
        if self.collection:
            self.collection_icon = "img/favorited.png"
        else:
            self.collection_icon = "img/unfavorited.png"
        self.qpb_star.setIcon(QIcon(self.collection_icon))

    # 显示单词的答案
    def show_answer(self):
        if pdt.setting["learning_mode"]:
            self.qpb_answer.setText(self.chinese)
        else:
            self.qpb_answer.setText(self.word)
        self.qpb_answer.setEnabled(False)

    # 标记单词为不认识
    def unfamiliar(self):
        self.change_w = "+5"
        self.close()

    # 标记单词为模糊
    def vague(self):
        self.change_w = "+2"
        self.close()

    # 标记单词为认识
    def know(self):
        self.change_w = "-2"
        self.close()

    # 标记单词为完全认识
    def mastered(self):
        if pdt.setting["confirm_complete"]:
            if QMessageBox.question(self, "提示", "你真的完全认识了吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.No:
                return
        self.change_w = "*0"
        pdt.menu.remove_words.append(self.word)
        self.close()

    # 显示单词的详细介绍
    def show_word_details(self):
        WordDetails(self.word, self.chinese).exec_()

    # 收藏图标的点击事件
    def star(self):
        if self.collection_icon == "img/favorited.png":
            self.collection_icon = "img/unfavorited.png"
        else:
            self.collection_icon = "img/favorited.png"
        self.qpb_star.setIcon(QIcon(self.collection_icon))

    # 在窗口关闭时调用，更新单词权重和收藏状态
    def closeEvent(self, event):
        asyncio.run(asyncio_c.set_w(pdt.phone, self.word, self.change_w))
        self.collection = pf.change_collection_state(self, self.collection, self.collection_icon, self.word, self.chinese)
        self.change_w = "+0"

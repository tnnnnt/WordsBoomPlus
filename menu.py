# coding:utf-8
import asyncio
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QMessageBox
import public_data as pdt
import asyncio_c
from feedback import Feedback
from head import Head
from help import Help
from inbox import Inbox
from personal_information import PersonalInformation
from ranking import Ranking
from search_word import SearchWord
from select_vocab_type import SelectVocabType
from setting import Setting
from collect_words import CollectWords
from test import Test
from word_popup import WordPopup


# 定义菜单窗口类
class Menu(QWidget):
    def __init__(self):
        super(Menu, self).__init__()
        # 设置窗口图标和标题
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("单词弹弹弹")

        # 创建窗口中的各个部件
        self.personal_information = PersonalInformation()
        self.select_vocab_type = SelectVocabType()
        self.setting = Setting()
        self.search_word = SearchWord()
        self.collect_words = CollectWords()
        self.test = Test()
        self.ranking = Ranking()
        self.feedback = Feedback()
        self.inbox = Inbox()
        self.help = Help()

        self.qt_popup = QTimer()
        self.round = 0
        self.words_popup = {}
        self.remove_words = []

        self.head = Head()
        self.head.show_head('img/head/' + pdt.avatar_num + '.jpg')
        self.ql_nickname = QLabel(pdt.nickname)
        self.qpb_run = QPushButton("启动")
        self.qpb_vocab = QPushButton(" 选择词书 ")
        self.qpb_setting = QPushButton("设置")
        self.qpb_search = QPushButton("查词")
        self.qpb_collect = QPushButton("收藏夹")
        self.qpb_test = QPushButton("词汇量测试")
        self.qpb_ranking = QPushButton("排行榜")
        self.qpb_feedback = QPushButton("反馈")
        self.qpb_inbox = QPushButton("收件箱")
        self.qpb_help = QPushButton(" 快速入门 ")
        self.qpb_recharge = QPushButton("充值")
        self.qpb_renew = QPushButton("检查更新")

        self.qgl = QGridLayout()
        self.qvbl = QVBoxLayout(self)

        # 设置各部件的字体和对齐方式
        self.ql_nickname.setFont(pdt.font0)
        self.ql_nickname.setAlignment(Qt.AlignCenter)
        self.qpb_run.setFont(pdt.font0)
        self.qpb_vocab.setFont(pdt.font0)
        self.qpb_setting.setFont(pdt.font0)
        self.qpb_search.setFont(pdt.font0)
        self.qpb_collect.setFont(pdt.font0)
        self.qpb_test.setFont(pdt.font0)
        self.qpb_ranking.setFont(pdt.font0)
        self.qpb_feedback.setFont(pdt.font0)
        self.qpb_inbox.setFont(pdt.font0)
        self.qpb_help.setFont(pdt.font0)
        self.qpb_recharge.setFont(pdt.font0)
        self.qpb_renew.setFont(pdt.font0)

        # 将各部件添加到布局中
        self.qgl.addWidget(self.qpb_run, 0, 0)
        self.qgl.addWidget(self.qpb_vocab, 0, 1)
        self.qgl.addWidget(self.qpb_setting, 0, 2)
        self.qgl.addWidget(self.qpb_search, 1, 0)
        self.qgl.addWidget(self.qpb_collect, 1, 1)
        self.qgl.addWidget(self.qpb_test, 1, 2)
        self.qgl.addWidget(self.qpb_ranking, 2, 0)
        self.qgl.addWidget(self.qpb_feedback, 2, 1)
        self.qgl.addWidget(self.qpb_inbox, 2, 2)
        self.qgl.addWidget(self.qpb_help, 3, 0)
        self.qgl.addWidget(self.qpb_recharge, 3, 1)
        self.qgl.addWidget(self.qpb_renew, 3, 2)

        self.qvbl.addWidget(self.head, alignment=Qt.AlignCenter)
        self.qvbl.addWidget(self.ql_nickname)
        self.qvbl.addLayout(self.qgl)

        # 连接各按钮的点击事件
        self.head.clicked.connect(self.personal_information.exec_)
        self.qpb_run.clicked.connect(self.run)
        self.qpb_vocab.clicked.connect(self.select_vocab_type.exec_)
        self.qpb_setting.clicked.connect(self.setting.exec_)
        self.qpb_search.clicked.connect(self.search_word.exec_)
        self.qpb_collect.clicked.connect(self.collect_words.exec_)
        self.qpb_test.clicked.connect(self.test.exec_)
        self.qpb_ranking.clicked.connect(self.ranking.exec_)
        self.qpb_feedback.clicked.connect(self.feedback.exec_)
        self.qpb_inbox.clicked.connect(self.inbox.exec_)
        self.qpb_help.clicked.connect(self.help.exec_)
        self.qpb_recharge.clicked.connect(self.recharge)
        self.qpb_renew.clicked.connect(self.renew)
        self.qt_popup.timeout.connect(self.show_word_popup)

        # 设置窗口大小并固定大小
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 启动或停止单词弹窗
    def run(self):
        if self.qpb_run.text() == "启动":
            self.remove_words = []
            self.round = 0
            self.qpb_run.setText("停止")
            self.qpb_test.setEnabled(False)
            self.show_word_popup()
        else:
            self.qt_popup.stop()
            self.qpb_run.setText("启动")
            self.qpb_test.setEnabled(True)

    # 弹出单词弹窗
    def show_word_popup(self):
        self.qt_popup.stop()
        if self.round >= pdt.setting["rounds_per_word"] or len(pdt.menu.words_popup) == 0:
            self.round = 0
        if self.round == 0:
            for _ in self.words_popup.values():
                del _
            self.words_popup = {}
            words = asyncio.run(asyncio_c.get_words(pdt.phone, pdt.setting["vocab"], pdt.setting["words_per_popup"]))
            for word in words:
                self.words_popup[word[0]] = WordPopup(word[0])
                self.words_popup[word[0]].set_word_popup()
                self.words_popup[word[0]].exec_()
        else:
            for word_popup in self.words_popup.values():
                word_popup.set_word_popup()
                word_popup.exec_()
        for remove_word in self.remove_words:
            if remove_word in self.words_popup:
                self.words_popup.pop(remove_word)
        self.remove_words = []
        self.qt_popup.start(pdt.ttt * pdt.setting["popup_cycle"])
        self.round += 1

    # 充值功能
    def recharge(self):
        QMessageBox.information(self, "充值", "您好！充值请联系\nQQ: " + pdt.QQ + "\n微信: " + pdt.wechat + "\n感谢您的支持！")

    # 检查更新功能
    def renew(self):
        new_version = asyncio.run(asyncio_c.get_new_version())
        if pdt.version == new_version:
            QMessageBox.information(self, "检查更新", "您好！您当前使用的版本为" + pdt.version + "\n是最新版本！\n感谢您的支持！")
        else:
            QMessageBox.information(self, "检查更新", "您好！您当前使用的版本为" + pdt.version + "\n最新版本为" + new_version + "\n请前往\nhttps://github.com/tnnnnt/WordsBoomPlus/releases\n下载最新版本！")

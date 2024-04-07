# coding:utf-8
import asyncio
from functools import partial
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QDialog, QHBoxLayout, QFrame
import WordsBoomPlus.public_data as pdt
import WordsBoomPlus.public_function as pf
from WordsBoomPlus import asyncio_c
from WordsBoomPlus.contribute import Contribute


# 定义单词详细信息类
class WordDetails(QDialog):
    # 初始化方法
    def __init__(self, word, chinese, favorite=None):
        super(WordDetails, self).__init__()
        self.setMinimumWidth(1200)
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("单词弹弹弹")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.word = word
        self.collection = favorite
        self.collection_icon = ""
        if self.collection == 1:
            self.collection_icon = "img/favorited.png"
        elif self.collection == 0:
            self.collection_icon = "img/unfavorited.png"
        self.chinese = chinese
        self.mnemonic = ""

        self.contribute = Contribute(self.word)
        self.qvbl = QVBoxLayout(self)

        # 设置单词显示控件
        self.ql_word = QLabel(self.word)
        self.ql_word.setFont(pdt.font2)
        self.ql_word.setAlignment(Qt.AlignCenter)
        self.qvbl.addWidget(self.ql_word)

        # 设置发音按钮和收藏按钮
        self.qpb_british = QPushButton("英音")
        self.qpb_british.setFont(pdt.font0)
        self.qpb_american = QPushButton("美音")
        self.qpb_american.setFont(pdt.font0)
        self.qpb_star = QPushButton()
        self.qhbl0 = QHBoxLayout()
        self.qhbl0.addWidget(self.qpb_british)
        if self.collection is not None:
            self.qpb_star.setStyleSheet("background-color:rgba(255,255,255,0)")
            self.qpb_star.setIcon(QIcon(self.collection_icon))
            self.qpb_star.setFixedSize(80, 80)
            self.qpb_star.setIconSize(QSize(80, 80))
            self.qpb_star.clicked.connect(self.star)
            self.qhbl0.addWidget(self.qpb_star)
        self.qhbl0.addWidget(self.qpb_american)
        self.qvbl.addLayout(self.qhbl0)

        # 设置发音按钮点击事件
        self.qpb_british.clicked.connect(partial(pf.audio_play, self.word, "1"))
        self.qpb_american.clicked.connect(partial(pf.audio_play, self.word, "2"))

        # 设置中文意思显示控件
        self.ql_chinese = QLabel(self.chinese)
        self.ql_chinese.setFont(pdt.font0)
        self.qvbl.addWidget(self.ql_chinese)

        # 获取例句及翻译
        self.example_sentences = asyncio.run(asyncio_c.get_example_sentences(self.word))
        self.qfs = [QFrame(), QFrame(), QFrame()]
        self.ql_sentences = [QLabel(self.example_sentences[0]), QLabel(self.example_sentences[1]), QLabel(self.example_sentences[2])]
        self.ql_translations = [QLabel(self.example_sentences[3]), QLabel(self.example_sentences[4]), QLabel(self.example_sentences[5])]
        for i in range(3):
            if self.example_sentences[i] == "":
                break
            self.qfs[i].setFrameShape(QFrame.HLine)
            self.qfs[i].setFrameShadow(QFrame.Sunken)
            self.ql_sentences[i].setFont(pdt.font0)
            self.ql_sentences[i].setAlignment(Qt.AlignLeft)
            self.ql_sentences[i].setMaximumHeight(400)
            self.ql_sentences[i].setWordWrap(True)
            self.ql_translations[i].setFont(pdt.font0)
            self.ql_translations[i].setAlignment(Qt.AlignLeft)
            self.ql_translations[i].setMaximumHeight(400)
            self.ql_translations[i].setWordWrap(True)
            self.qvbl.addWidget(self.qfs[i])
            self.qvbl.addWidget(self.ql_sentences[i])
            self.qvbl.addWidget(self.ql_translations[i])

        # 设置助记显示控件
        self.qf = QFrame()
        self.qf.setFrameShape(QFrame.HLine)
        self.qf.setFrameShadow(QFrame.Sunken)
        self.ql = QLabel("助记")
        self.ql.setFont(pdt.font0)
        self.ql.setAlignment(Qt.AlignCenter)
        self.ql_mnemonic = QLabel()
        self.ql_contributor_name = QLabel()
        self.change()
        self.ql_mnemonic.setFont(pdt.font0)
        self.ql_mnemonic.setAlignment(Qt.AlignCenter)
        self.ql_contributor = QLabel("贡献者：")
        self.ql_contributor.setFont(pdt.font1)
        self.ql_contributor.setAlignment(Qt.AlignRight)
        self.ql_contributor_name.setFont(pdt.font1)
        self.ql_contributor_name.setAlignment(Qt.AlignLeft)
        self.qhbl1 = QHBoxLayout()
        self.qhbl1.addWidget(self.ql_contributor)
        self.qhbl1.addWidget(self.ql_contributor_name)
        self.qpb_change = QPushButton("换个助记")
        self.qpb_change.setFont(pdt.font0)
        self.qpb_contribute = QPushButton("贡献助记")
        self.qpb_contribute.setFont(pdt.font0)
        self.qhbl2 = QHBoxLayout()
        self.qhbl2.addWidget(self.qpb_change)
        self.qhbl2.addWidget(self.qpb_contribute)
        self.qvbl.addWidget(self.qf)
        self.qvbl.addWidget(self.ql)
        self.qvbl.addWidget(self.ql_mnemonic)
        self.qvbl.addLayout(self.qhbl1)
        self.qvbl.addLayout(self.qhbl2)
        self.qpb_change.clicked.connect(self.change)
        self.qpb_contribute.clicked.connect(self.contribute.exec_)

    # 收藏图标点击事件
    def star(self):
        if self.collection_icon == "img/favorited.png":
            self.collection_icon = "img/unfavorited.png"
        else:
            self.collection_icon = "img/favorited.png"
        self.qpb_star.setIcon(QIcon(self.collection_icon))

    # 更新助记
    def change(self):
        self.mnemonic = asyncio.run(asyncio_c.get_mnemonic(self.word))
        if self.mnemonic is None:
            self.ql_mnemonic.setText("暂无助记，等您发挥")
            self.ql_contributor_name.setText("无")
        else:
            self.ql_mnemonic.setText(self.mnemonic[0])
            self.ql_contributor_name.setText(self.mnemonic[1])

    # 在窗口关闭时保存收藏状态
    def closeEvent(self, event):
        self.collection = pf.change_collection_state(self, self.collection, self.collection_icon, self.word, self.chinese)

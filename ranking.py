# coding:utf-8
import asyncio
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDialog, QHBoxLayout, QWidget, QScrollArea, QGridLayout
import WordsBoomPlus.public_data as pdt
from WordsBoomPlus import asyncio_c


# 单个排行榜项
class OneRank(QWidget):
    def __init__(self, rank, avatar_num, nickname, num):
        super(OneRank, self).__init__()
        self.ql_rank = QLabel("第" + str(rank) + "名")
        self.ql_avatar = QLabel()
        self.ql_avatar.setPixmap(QPixmap('img/head/' + str(avatar_num) + '.jpg').scaled(60, 60))
        self.ql_nickname = QLabel(nickname)
        self.ql_num = QLabel(str(num))

        # 设置控件属性
        self.ql_rank.setFont(pdt.font0)
        self.ql_rank.setMinimumWidth(100)
        self.ql_rank.setAlignment(Qt.AlignCenter)
        self.ql_nickname.setFont(pdt.font0)
        self.ql_nickname.setMinimumWidth(360)
        self.ql_nickname.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.ql_num.setFont(pdt.font0)
        self.ql_num.setMinimumWidth(100)
        self.ql_num.setAlignment(Qt.AlignCenter)

        self.qhbl = QHBoxLayout(self)
        self.qhbl.addWidget(self.ql_rank)
        self.qhbl.addWidget(self.ql_avatar)
        self.qhbl.addWidget(self.ql_nickname)
        self.qhbl.addWidget(self.ql_num)

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())


# 排行榜类
class Ranking(QDialog):
    def __init__(self):
        super(Ranking, self).__init__()
        self.setFixedSize(1600, 900)
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("排行榜")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # 获取全局排行榜数据
        vocabulary_rank = asyncio.run(asyncio_c.get_vocabulary_rank())
        mnemonic_rank = asyncio.run(asyncio_c.get_mnemonic_rank())

        # 设置词汇量排行榜标题
        self.ql_title_vocabulary = QLabel("词汇量排行榜")
        self.ql_title_vocabulary.setFont(pdt.font2)
        self.ql_title_vocabulary.setMinimumHeight(60)
        self.ql_title_vocabulary.setAlignment(Qt.AlignCenter)

        # 设置助记贡献排行榜标题
        self.ql_title_mnemonic = QLabel("助记贡献排行榜")
        self.ql_title_mnemonic.setFont(pdt.font2)
        self.ql_title_mnemonic.setMinimumHeight(60)
        self.ql_title_mnemonic.setAlignment(Qt.AlignCenter)

        # 创建词汇量排行榜控件
        self.qvbl_vocabulary = QVBoxLayout()
        self.qw_vocabulary = QWidget()
        self.qw_vocabulary.setLayout(self.qvbl_vocabulary)
        self.qsa_vocabulary = QScrollArea()
        self.qsa_vocabulary.setWidgetResizable(True)  # 设置滚动区域的大小调整策略
        self.qsa_vocabulary.setWidget(self.qw_vocabulary)
        for i in range(len(vocabulary_rank)):
            self.qvbl_vocabulary.addWidget(
                OneRank(i + 1, vocabulary_rank[i][0], vocabulary_rank[i][1], vocabulary_rank[i][2]))

        # 创建助记贡献排行榜控件
        self.qvbl_mnemonic = QVBoxLayout()
        self.qw_mnemonic = QWidget()
        self.qw_mnemonic.setLayout(self.qvbl_mnemonic)
        self.qsa_mnemonic = QScrollArea()
        self.qsa_mnemonic.setWidgetResizable(True)  # 设置滚动区域的大小调整策略
        self.qsa_mnemonic.setWidget(self.qw_mnemonic)
        for i in range(len(mnemonic_rank)):
            self.qvbl_mnemonic.addWidget(OneRank(i + 1, mnemonic_rank[i][0], mnemonic_rank[i][1], mnemonic_rank[i][2]))

        # 创建个人排行榜项
        self.or_personal_vocabulary_rank = OneRank(asyncio.run(asyncio_c.get_personal_vocabulary_rank(pdt.phone)), pdt.avatar_num, pdt.nickname, pdt.vocabulary)
        personal_mnemonic_rank = asyncio.run(asyncio_c.get_personal_mnemonic_rank(pdt.phone))
        self.or_personal_mnemonic_rank = OneRank(personal_mnemonic_rank[1], pdt.avatar_num, pdt.nickname, personal_mnemonic_rank[0])

        # 布局排行榜控件
        self.qgl = QGridLayout(self)
        self.qgl.addWidget(self.ql_title_vocabulary, 0, 0)
        self.qgl.addWidget(self.ql_title_mnemonic, 0, 1)
        self.qgl.addWidget(self.qsa_vocabulary, 1, 0)
        self.qgl.addWidget(self.qsa_mnemonic, 1, 1)
        self.qgl.addWidget(self.or_personal_vocabulary_rank, 2, 0)
        self.qgl.addWidget(self.or_personal_mnemonic_rank, 2, 1)
        self.qgl.setSpacing(0)
        self.qgl.setContentsMargins(0, 0, 0, 0)

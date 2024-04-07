# coding:utf-8
import asyncio
import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QPushButton, QGridLayout, QWidget, QLabel, QVBoxLayout, QMessageBox, QScrollArea
import WordsBoomPlus.public_data as pdt
from WordsBoomPlus import asyncio_c


# 定义词书类
class Vocab(QWidget):
    def __init__(self, img, name, num):
        super(Vocab, self).__init__()
        self.img = img
        # 设置词书图片
        self.ql_img = QLabel()
        self.ql_img.setPixmap(QPixmap('img/vocab/' + self.img + '.jpg').scaled(200, 270))
        self.ql_img.setScaledContents(True)
        # 设置词书名称
        self.ql_name = QLabel(name)
        self.ql_name.setFont(pdt.font1)
        # 设置单词数量
        self.ql_num = QLabel("单词数：" + str(num))
        self.ql_num.setFont(pdt.font1)
        # 设置按钮
        self.qpb_sure = QPushButton("就这个了")
        self.qpb_sure.setFont(pdt.font0)
        self.qpb_reset_w = QPushButton("重置权重")
        self.qpb_reset_w.setFont(pdt.font0)

        self.qvbl = QVBoxLayout(self)
        self.qvbl.addWidget(self.ql_img)
        self.qvbl.addWidget(self.ql_name)
        self.qvbl.addWidget(self.ql_num)
        self.qvbl.addWidget(self.qpb_sure)
        self.qvbl.addWidget(self.qpb_reset_w)

        self.qpb_sure.clicked.connect(self.change_vocab)
        self.qpb_reset_w.clicked.connect(self.reset_w)

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 切换词书
    def change_vocab(self):
        if pdt.setting['vocab'] != self.img:
            pdt.setting['vocab'] = self.img
            with open('setting.json', 'w', encoding='utf-8') as f:
                json.dump(pdt.setting, f)
        QMessageBox.information(self, "成功", "切换成功！")

    # 重置权重
    def reset_w(self):
        reply = QMessageBox.question(self, "警告", "你真的要重置权重吗？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            asyncio.run(asyncio_c.reset_w(pdt.phone, self.img))
            QMessageBox.information(self, "成功", "权重重置成功！")


# 小学词书选择界面
class PrimaryVocab(QDialog):
    def __init__(self):
        super(PrimaryVocab, self).__init__()
        self.setFixedSize(1000, 900)
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("选择小学词书")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.vocab1 = Vocab("pepxiaoxue,1", "人教版小学英语-三年级上册", 59)
        self.vocab2 = Vocab("pepxiaoxue,2", "人教版小学英语-三年级下册", 71)
        self.vocab3 = Vocab("pepxiaoxue,3", "人教版小学英语-四年级上册", 70)
        self.vocab4 = Vocab("pepxiaoxue,4", "人教版小学英语-四年级下册", 76)
        self.vocab5 = Vocab("pepxiaoxue,5", "人教版小学英语-五年级上册", 106)
        self.vocab6 = Vocab("pepxiaoxue,6", "人教版小学英语-五年级下册", 122)
        self.vocab7 = Vocab("pepxiaoxue,7", "人教版小学英语-六年级上册", 105)
        self.vocab8 = Vocab("pepxiaoxue,8", "人教版小学英语-六年级下册", 100)

        self.qgl = QGridLayout()
        self.qw = QWidget()
        self.qw.setLayout(self.qgl)
        self.qsa = QScrollArea()
        self.qsa.setWidgetResizable(True)  # 设置滚动区域的大小调整策略
        self.qsa.setWidget(self.qw)
        self.qvbl = QVBoxLayout(self)
        self.qvbl.setSpacing(0)
        self.qvbl.setContentsMargins(0, 0, 0, 0)
        self.qvbl.addWidget(self.qsa)
        self.qgl.addWidget(self.vocab1, 0, 0)
        self.qgl.addWidget(self.vocab2, 0, 1)
        self.qgl.addWidget(self.vocab3, 0, 2)
        self.qgl.addWidget(self.vocab4, 0, 3)
        self.qgl.addWidget(self.vocab5, 1, 0)
        self.qgl.addWidget(self.vocab6, 1, 1)
        self.qgl.addWidget(self.vocab7, 1, 2)
        self.qgl.addWidget(self.vocab8, 1, 3)


# 初中词书选择界面
class MiddleVocab(QDialog):
    def __init__(self):
        super(MiddleVocab, self).__init__()
        self.setFixedSize(800, 900)
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("选择初中词书")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.vocab1 = Vocab("pepchuzhong,1", "人教版初中英语-七年级上册", 350)
        self.vocab2 = Vocab("pepchuzhong,2", "人教版初中英语-七年级下册", 396)
        self.vocab3 = Vocab("pepchuzhong,3", "人教版初中英语-八年级上册", 340)
        self.vocab4 = Vocab("pepchuzhong,4", "人教版初中英语-八年级下册", 359)
        self.vocab5 = Vocab("pepchuzhong,5", "人教版初中英语-九年级全册", 479)
        self.vocab6 = Vocab("waiyanshechuzhong,1", "外研社版初中英语-七年级上册", 470)
        self.vocab7 = Vocab("waiyanshechuzhong,2", "外研社版初中英语-七年级下册", 328)
        self.vocab8 = Vocab("waiyanshechuzhong,3", "外研社版初中英语-八年级上册", 254)
        self.vocab9 = Vocab("waiyanshechuzhong,4", "外研社版初中英语-八年级上册", 207)
        self.vocab10 = Vocab("waiyanshechuzhong,5", "外研社版初中英语-九年级上册", 294)
        self.vocab11 = Vocab("waiyanshechuzhong,6", "外研社版初中英语-九年级上册", 104)
        self.vocab12 = Vocab("chuzhong_2,1", "初中英语词汇", 1418)
        self.vocab13 = Vocab("chuzhong_3,1", "新东方初中词汇", 1803)

        self.qgl = QGridLayout()
        self.qw = QWidget()
        self.qw.setLayout(self.qgl)
        self.qsa = QScrollArea()
        self.qsa.setWidgetResizable(True)  # 设置滚动区域的大小调整策略
        self.qsa.setWidget(self.qw)
        self.qvbl = QVBoxLayout(self)
        self.qvbl.setSpacing(0)
        self.qvbl.setContentsMargins(0, 0, 0, 0)
        self.qvbl.addWidget(self.qsa)
        self.qgl.addWidget(self.vocab1, 0, 0)
        self.qgl.addWidget(self.vocab2, 0, 1)
        self.qgl.addWidget(self.vocab3, 0, 2)
        self.qgl.addWidget(self.vocab4, 1, 0)
        self.qgl.addWidget(self.vocab5, 1, 1)
        self.qgl.addWidget(self.vocab6, 2, 0)
        self.qgl.addWidget(self.vocab7, 2, 1)
        self.qgl.addWidget(self.vocab8, 2, 2)
        self.qgl.addWidget(self.vocab9, 3, 0)
        self.qgl.addWidget(self.vocab10, 3, 1)
        self.qgl.addWidget(self.vocab11, 3, 2)
        self.qgl.addWidget(self.vocab12, 4, 0)
        self.qgl.addWidget(self.vocab13, 4, 1)


# 高中词书选择界面
class HighVocab(QDialog):
    def __init__(self):
        super(HighVocab, self).__init__()
        self.setFixedSize(1000, 900)
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("选择高中词书")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.vocab1 = Vocab("pepgaozhong,1", "人教版高中英语-必修 1", 218)
        self.vocab2 = Vocab("pepgaozhong,2", "人教版高中英语-必修 2", 224)
        self.vocab3 = Vocab("pepgaozhong,3", "人教版高中英语-必修 3", 273)
        self.vocab4 = Vocab("pepgaozhong,4", "人教版高中英语-必修 4", 224)
        self.vocab5 = Vocab("pepgaozhong,5", "人教版高中英语-必修 5", 268)
        self.vocab6 = Vocab("pepgaozhong,6", "人教版高中英语-选修 6", 270)
        self.vocab7 = Vocab("pepgaozhong,7", "人教版高中英语-选修 7", 295)
        self.vocab8 = Vocab("pepgaozhong,8", "人教版高中英语-选修 8", 297)
        self.vocab9 = Vocab("pepgaozhong,9", "人教版高中英语-选修 9", 314)
        self.vocab10 = Vocab("pepgaozhong,10", "人教版高中英语-选修 10", 308)
        self.vocab11 = Vocab("pepgaozhong,11", "人教版高中英语-选修 11", 265)
        self.vocab12 = Vocab("beishigaozhong,1", "北师大版高中必修一", 191)
        self.vocab13 = Vocab("beishigaozhong,2", "北师大版高中必修二", 213)
        self.vocab14 = Vocab("beishigaozhong,3", "北师大版高中必修三", 246)
        self.vocab15 = Vocab("beishigaozhong,4", "北师大版高中必修四", 309)
        self.vocab16 = Vocab("beishigaozhong,5", "北师大版高中必修五", 292)
        self.vocab17 = Vocab("beishigaozhong,6", "北师大版高中选修六", 217)
        self.vocab18 = Vocab("beishigaozhong,7", "北师大版高中选修七", 304)
        self.vocab19 = Vocab("beishigaozhong,8", "北师大版高中选修八", 290)
        self.vocab20 = Vocab("beishigaozhong,9", "北师大版高中选修九", 260)
        self.vocab21 = Vocab("beishigaozhong,10", "北师大版高中选修十", 249)
        self.vocab22 = Vocab("beishigaozhong,11", "北师大版高中选修十一", 316)
        self.vocab23 = Vocab("gaozhong_2,1", "高中英语词汇", 3665)

        self.qgl = QGridLayout()
        self.qw = QWidget()
        self.qw.setLayout(self.qgl)
        self.qsa = QScrollArea()
        self.qsa.setWidgetResizable(True)  # 设置滚动区域的大小调整策略
        self.qsa.setWidget(self.qw)
        self.qvbl = QVBoxLayout(self)
        self.qvbl.setSpacing(0)
        self.qvbl.setContentsMargins(0, 0, 0, 0)
        self.qvbl.addWidget(self.qsa)
        self.qgl.addWidget(self.vocab1, 0, 0)
        self.qgl.addWidget(self.vocab2, 0, 1)
        self.qgl.addWidget(self.vocab3, 0, 2)
        self.qgl.addWidget(self.vocab4, 0, 3)
        self.qgl.addWidget(self.vocab5, 1, 0)
        self.qgl.addWidget(self.vocab6, 1, 1)
        self.qgl.addWidget(self.vocab7, 1, 2)
        self.qgl.addWidget(self.vocab8, 1, 3)
        self.qgl.addWidget(self.vocab9, 2, 0)
        self.qgl.addWidget(self.vocab10, 2, 1)
        self.qgl.addWidget(self.vocab11, 2, 2)
        self.qgl.addWidget(self.vocab12, 3, 0)
        self.qgl.addWidget(self.vocab13, 3, 1)
        self.qgl.addWidget(self.vocab14, 3, 2)
        self.qgl.addWidget(self.vocab15, 3, 3)
        self.qgl.addWidget(self.vocab16, 4, 0)
        self.qgl.addWidget(self.vocab17, 4, 1)
        self.qgl.addWidget(self.vocab18, 4, 2)
        self.qgl.addWidget(self.vocab19, 4, 3)
        self.qgl.addWidget(self.vocab20, 5, 0)
        self.qgl.addWidget(self.vocab21, 5, 1)
        self.qgl.addWidget(self.vocab22, 5, 2)
        self.qgl.addWidget(self.vocab23, 6, 0)


# 大学词书选择界面
class UniversityVocab(QDialog):
    def __init__(self):
        super(UniversityVocab, self).__init__()
        self.setFixedSize(800, 900)
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("选择大学词书")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.vocab1 = Vocab("cet4_1,1", "四级真题核心词", 1162)
        self.vocab2 = Vocab("cet4_2,1", "四级英语词汇", 3739)
        self.vocab3 = Vocab("cet4_3,1", "新东方四级词汇", 2607)
        self.vocab4 = Vocab("cet6_1,1", "六级真题核心词", 1228)
        self.vocab5 = Vocab("cet6_2,1", "六级英语词汇", 2078)
        self.vocab6 = Vocab("cet6_3,1", "新东方六级词汇", 2345)
        self.vocab7 = Vocab("kaoyan_1,1", "考研必考词汇", 1340)
        self.vocab8 = Vocab("kaoyan_2,1", "考研英语词汇", 4533)
        self.vocab9 = Vocab("kaoyan_3,1", "新东方考研词汇", 3727)
        self.vocab10 = Vocab("level4_1,1", "专四真题高频词", 595)
        self.vocab11 = Vocab("level4_2,1", "专四核心词汇", 4025)
        self.vocab12 = Vocab("level8_1,1", "专八真题高频词", 684)
        self.vocab13 = Vocab("level8_2,1", "专八核心词汇", 12197)

        self.qgl = QGridLayout()
        self.qw = QWidget()
        self.qw.setLayout(self.qgl)
        self.qsa = QScrollArea()
        self.qsa.setWidgetResizable(True)  # 设置滚动区域的大小调整策略
        self.qsa.setWidget(self.qw)
        self.qvbl = QVBoxLayout(self)
        self.qvbl.setSpacing(0)
        self.qvbl.setContentsMargins(0, 0, 0, 0)
        self.qvbl.addWidget(self.qsa)
        self.qgl.addWidget(self.vocab1, 0, 0)
        self.qgl.addWidget(self.vocab2, 0, 1)
        self.qgl.addWidget(self.vocab3, 0, 2)
        self.qgl.addWidget(self.vocab4, 1, 0)
        self.qgl.addWidget(self.vocab5, 1, 1)
        self.qgl.addWidget(self.vocab6, 1, 2)
        self.qgl.addWidget(self.vocab7, 2, 0)
        self.qgl.addWidget(self.vocab8, 2, 1)
        self.qgl.addWidget(self.vocab9, 2, 2)
        self.qgl.addWidget(self.vocab10, 3, 0)
        self.qgl.addWidget(self.vocab11, 3, 1)
        self.qgl.addWidget(self.vocab12, 4, 0)
        self.qgl.addWidget(self.vocab13, 4, 1)


# 留学词书选择界面
class AbroadVocab(QDialog):
    def __init__(self):
        super(AbroadVocab, self).__init__()
        self.setFixedSize(1000, 900)
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("选择留学词书")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.vocab1 = Vocab("ielts_2,1", "雅思词汇", 3427)
        self.vocab2 = Vocab("ielts_3,1", "新东方雅思词汇", 3555)
        self.vocab3 = Vocab("toefl_2,1", "TOEFL 词汇", 9212)
        self.vocab4 = Vocab("toefl_3,1", "新东方 TOEFL 词汇", 4264)
        self.vocab5 = Vocab("sat_2,1", "SAT 词汇", 4423)
        self.vocab6 = Vocab("sat_3,1", "新东方 SAT 词汇", 4438)
        self.vocab7 = Vocab("gre_2,1", "GRE 词汇", 7199)
        self.vocab8 = Vocab("gre_3,1", "新东方 GRE 词汇", 6514)
        self.vocab9 = Vocab("gmat_2,1", "GMAT 词汇", 3254)
        self.vocab10 = Vocab("gmat_3,1", "新东方 GMAT 词汇", 3037)

        self.qgl = QGridLayout()
        self.qw = QWidget()
        self.qw.setLayout(self.qgl)
        self.qsa = QScrollArea()
        self.qsa.setWidgetResizable(True)  # 设置滚动区域的大小调整策略
        self.qsa.setWidget(self.qw)
        self.qvbl = QVBoxLayout(self)
        self.qvbl.setSpacing(0)
        self.qvbl.setContentsMargins(0, 0, 0, 0)
        self.qvbl.addWidget(self.qsa)
        self.qgl.addWidget(self.vocab1, 0, 0)
        self.qgl.addWidget(self.vocab2, 0, 1)
        self.qgl.addWidget(self.vocab3, 0, 2)
        self.qgl.addWidget(self.vocab4, 0, 3)
        self.qgl.addWidget(self.vocab5, 1, 0)
        self.qgl.addWidget(self.vocab6, 1, 1)
        self.qgl.addWidget(self.vocab7, 1, 2)
        self.qgl.addWidget(self.vocab8, 1, 3)
        self.qgl.addWidget(self.vocab9, 2, 0)
        self.qgl.addWidget(self.vocab10, 2, 1)


# 商务词书选择界面
class CommercialVocab(QDialog):
    def __init__(self):
        super(CommercialVocab, self).__init__()
        self.setFixedSize(600, 450)
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("选择商务词书")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        self.vocab1 = Vocab("bec_2,1", "商务英语词汇", 2753)
        self.vocab2 = Vocab("bec_3,1", "新东方 BEC 词汇", 2824)

        self.qgl = QGridLayout()
        self.qw = QWidget()
        self.qw.setLayout(self.qgl)
        self.qsa = QScrollArea()
        self.qsa.setWidgetResizable(True)  # 设置滚动区域的大小调整策略
        self.qsa.setWidget(self.qw)
        self.qvbl = QVBoxLayout(self)
        self.qvbl.setSpacing(0)
        self.qvbl.setContentsMargins(0, 0, 0, 0)
        self.qvbl.addWidget(self.qsa)
        self.qgl.addWidget(self.vocab1, 0, 0)
        self.qgl.addWidget(self.vocab2, 0, 1)


# 选择词书类型对话框类
class SelectVocabType(QDialog):
    def __init__(self):
        super(SelectVocabType, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("选择词书类型")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # 创建各种词书的实例
        self.primary_vocab = PrimaryVocab()
        self.middle_vocab = MiddleVocab()
        self.high_vocab = HighVocab()
        self.university_vocab = UniversityVocab()
        self.abroad_vocab = AbroadVocab()
        self.commercial_vocab = CommercialVocab()

        # 创建各种类型的按钮
        self.qpb_primary = QPushButton("小学")
        self.qpb_middle = QPushButton("初中")
        self.qpb_high = QPushButton("高中")
        self.qpb_university = QPushButton("大学")
        self.qpb_abroad = QPushButton("留学")
        self.qpb_commercial = QPushButton("商务")

        # 设置按钮字体
        self.qpb_primary.setFont(pdt.font0)
        self.qpb_middle.setFont(pdt.font0)
        self.qpb_high.setFont(pdt.font0)
        self.qpb_university.setFont(pdt.font0)
        self.qpb_abroad.setFont(pdt.font0)
        self.qpb_commercial.setFont(pdt.font0)

        # 将按钮添加到布局中
        self.qgl = QGridLayout(self)
        self.qgl.addWidget(self.qpb_primary, 0, 0)
        self.qgl.addWidget(self.qpb_middle, 0, 1)
        self.qgl.addWidget(self.qpb_high, 0, 2)
        self.qgl.addWidget(self.qpb_university, 1, 0)
        self.qgl.addWidget(self.qpb_abroad, 1, 1)
        self.qgl.addWidget(self.qpb_commercial, 1, 2)

        # 连接按钮的点击事件到对应的槽函数
        self.qpb_primary.clicked.connect(self.show_primary_vocab)
        self.qpb_middle.clicked.connect(self.show_middle_vocab)
        self.qpb_high.clicked.connect(self.show_high_vocab)
        self.qpb_university.clicked.connect(self.show_university_vocab)
        self.qpb_abroad.clicked.connect(self.show_abroad_vocab)
        self.qpb_commercial.clicked.connect(self.show_commercial_vocab)

        # 调整窗口大小并固定大小
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 显示小学词书界面
    def show_primary_vocab(self):
        self.hide()
        self.primary_vocab.exec_()

    # 显示初中词书界面
    def show_middle_vocab(self):
        self.hide()
        self.middle_vocab.exec_()

    # 显示高中词书界面
    def show_high_vocab(self):
        self.hide()
        self.high_vocab.exec_()

    # 显示大学词书界面
    def show_university_vocab(self):
        self.hide()
        self.university_vocab.exec_()

    # 显示留学词书界面
    def show_abroad_vocab(self):
        self.hide()
        self.abroad_vocab.exec_()

    # 显示商务词书界面
    def show_commercial_vocab(self):
        self.hide()
        self.commercial_vocab.exec_()

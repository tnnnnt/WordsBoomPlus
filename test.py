# coding:utf-8
import asyncio
import random
import public_function as pf
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QDialog, QMessageBox
import public_data as pdt
import asyncio_c


# 单词问题界面类
class Question(QDialog):
    def __init__(self, word, chinese, wrong_chinese_s):
        super(Question, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("词汇量测试")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint & ~Qt.WindowCloseButtonHint)

        # 初始化计时器和倒计时时间
        self.time = 10
        self.ql_word = QLabel(word)  # 单词标签
        self.ql_time = QLabel("10")  # 倒计时标签
        self.qt_time = QTimer()  # 计时器
        self.qt_time.timeout.connect(self.reduce_time)
        # 四个中文释义按钮和一个不认识按钮
        self.qpb_chinese_s = [QPushButton(chinese), QPushButton(wrong_chinese_s[0]), QPushButton(wrong_chinese_s[1]),
                              QPushButton(wrong_chinese_s[2])]
        self.qpb_unfamiliar = QPushButton("不认识")

        # 设置字体和布局
        self.ql_word.setFont(pdt.font2)
        self.ql_word.setAlignment(Qt.AlignCenter)
        self.ql_time.setFont(pdt.font0)
        self.ql_time.setAlignment(Qt.AlignCenter)
        for qpb in self.qpb_chinese_s:
            qpb.setFont(pdt.font0)
            qpb.setFixedSize(QSize(1600, 200))
        self.qpb_unfamiliar.setFont(pdt.font0)

        # 点击事件绑定
        self.qpb_chinese_s[0].clicked.connect(self.right)
        for i in range(1, 4):
            self.qpb_chinese_s[i].clicked.connect(self.wrong)
        random.shuffle(self.qpb_chinese_s)
        self.qpb_unfamiliar.clicked.connect(self.unfamiliar)

        # 布局管理
        self.qvbl = QVBoxLayout(self)
        self.qvbl.addWidget(self.ql_word)
        self.qvbl.addWidget(self.ql_time)
        for qpb in self.qpb_chinese_s:
            self.qvbl.addWidget(qpb)
        self.qvbl.addWidget(self.qpb_unfamiliar)

        # 调整窗口大小
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
        # 启动计时器
        self.qt_time.start(1000)

    # 答对处理
    def right(self):
        # 播放正确提示音
        if pdt.setting['right_sound']:
            word = random.choice(["nice", "great", "unbelievable", "wonderful", "amazing", "good"])
            type = random.choice(["1", "2"])
            pf.audio_play(word, type)
        pdt.menu.test.right += 1
        self.close()

    # 答错处理
    def wrong(self):
        # 播放错误提示音
        if pdt.setting['wrong_sound']:
            word = random.choice(["shit", "yee"])
            type = random.choice(["1", "2"])
            pf.audio_play(word, type)
        pdt.menu.test.wrong += 2
        self.close()

    # 不认识处理
    def unfamiliar(self):
        pdt.menu.test.wrong += 1
        self.close()

    # 倒计时处理
    def reduce_time(self):
        self.time -= 1
        self.ql_time.setText(str(self.time))
        if self.time == 0:
            self.wrong()


# 显示问题界面
def show_question():
    words_and_chinese_s = asyncio.run(asyncio_c.get_words_and_chinese_s())
    for word, chinese in words_and_chinese_s:
        wrong_chinese_s = asyncio.run(asyncio_c.get_wrong_chinese_s(word))
        Question(word, chinese, wrong_chinese_s).exec_()


# 词汇量测试类
class Test(QDialog):
    def __init__(self):
        super(Test, self).__init__()
        # 设置窗口图标、标题和模态对话框等属性
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("词汇量测试")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        # 初始化答对和答错数量
        self.right, self.wrong = 0, 0

        # 词汇量标签和开始测试按钮
        self.ql_vocabulary = QLabel("您的词汇量：" + str(pdt.vocabulary))
        self.ql_vocabulary.setFont(pdt.font2)
        self.ql_vocabulary.setAlignment(Qt.AlignCenter)
        self.qpb_start = QPushButton("开始测试")
        self.qpb_start.setFont(pdt.font0)
        self.qpb_start.clicked.connect(self.start)

        # 查看规则按钮
        self.qpb_rule = QPushButton("查看规则")
        self.qpb_rule.setFont(pdt.font0)
        self.qpb_rule.clicked.connect(self.show_rule)

        # 布局管理
        self.qvbl = QVBoxLayout(self)
        self.qvbl.addWidget(self.ql_vocabulary)
        self.qvbl.addWidget(self.qpb_start)
        self.qvbl.addWidget(self.qpb_rule)

        # 调整窗口大小
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 开始测试
    def start(self):
        self.right, self.wrong = 0, 0
        # 连续出题，直到答错一定数量或用户选择结束测试
        for _ in range(6):
            show_question()
        while self.wrong == 0:
            show_question()
        while True:
            if QMessageBox.question(self, "提示", "再来一组（每组5个）？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.No:
                break
            show_question()
        # 计算词汇量并保存到数据库
        pdt.vocabulary = int(self.right * 20000 / (self.right + self.wrong))
        asyncio.run(asyncio_c.set_vocabulary(pdt.phone, pdt.vocabulary))
        # 显示测试结果
        QMessageBox.information(self, "测试结果", "您的词汇量预估为"+str(pdt.vocabulary)+"个单词")
        self.ql_vocabulary.setText("您的词汇量：" + str(pdt.vocabulary))

    # 显示测试规则
    def show_rule(self):
        QMessageBox.information(self, "测试规则", "对于弹出的每个单词\n请在10秒内选择您认为正确的中文释义\n超时将视为错误\n如果不认识请尽量点击不认识\n点击不认识比选错的影响小一些\n当测试达到一定量后会询问是否继续\n此时可以选择继续测试或结束测试")

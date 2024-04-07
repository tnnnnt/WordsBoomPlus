# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QDialog
import WordsBoomPlus.public_data as pdt


# 帮助窗口类
class Help(QDialog):
    def __init__(self):
        super(Help, self).__init__()
        self.setFixedSize(1800, 900)
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("快速入门")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        # 创建标签，并设置显示的文本和样式
        self.ql_img_menu = QLabel()
        self.ql_img_setting = QLabel()
        self.ql_img_popup = QLabel()
        self.ql_img_detail = QLabel()
        self.ql_img_menu.setPixmap(QPixmap('img/help/menu.png'))
        self.ql_img_setting.setPixmap(QPixmap('img/help/setting.png'))
        self.ql_img_popup.setPixmap(QPixmap('img/help/popup.png'))
        self.ql_img_detail.setPixmap(QPixmap('img/help/detail.png'))
        self.ql_img_menu.setAlignment(Qt.AlignCenter)
        self.ql_img_setting.setAlignment(Qt.AlignCenter)
        self.ql_img_popup.setAlignment(Qt.AlignCenter)
        self.ql_img_detail.setAlignment(Qt.AlignCenter)

        self.ql_text_start = QLabel("\n如果您是第一次使用该软件，还请耐心看下快速入门的基本操作。\n")
        self.ql_text_menu = QLabel("\n如图是主菜单，这里只介绍几个必备的使用方法，其余的功能请自行探索。\n")
        self.ql_text_choice_vocab = QLabel("\n点击主菜单的“选择词书”按钮，选择您想要学习的词书。\n")
        self.ql_text_setting = QLabel("\n点击主菜单的“设置”按钮，可以按自己的需要自定义设置。\n其中“完全认识防误操作”可以在误点击“完全认识”按钮时弹出确认窗口，“取消收藏防误操作”同理。\n“正确音效”与“错误音效”是在“词汇量测试”时的音效设置。\n其他功能在下一步中再详细介绍。\n后续步骤假设按如图设置。\n")
        self.ql_text_popup = QLabel("\n点击主菜单的“启动”按钮，即可启动单词弹窗。\n下面介绍按预先的设置。\n每3分钟弹出一组单词，每组单词3个，且需记忆2轮。\n先尝试回忆该词的中文，然后点击“查看答案”按钮检验。\n点击“详细介绍”可以查看单词的详细介绍（具体看下一步）。\n点亮爱心图标可以收藏该单词。\n根据实际情况点击“不认识”、“模糊”、“认识”、“完全认识”，会对该单词的权重进行重新计算，影响后续该单词出现的概率。\n")
        self.ql_text_detail = QLabel("\n点击单词弹窗的“详细介绍”按钮，可以查看该单词的详细介绍。\n包括英文、中文、发音、例句、助记。\n")
        self.ql_text_end = QLabel("\n以上就是快速入门的使用方法，如果您之后忘了怎么使用，请点击主菜单的“快速入门”按钮。\n")
        self.ql_text_start.setFont(pdt.font0)
        self.ql_text_menu.setFont(pdt.font0)
        self.ql_text_choice_vocab.setFont(pdt.font0)
        self.ql_text_setting.setFont(pdt.font0)
        self.ql_text_popup.setFont(pdt.font0)
        self.ql_text_detail.setFont(pdt.font0)
        self.ql_text_end.setFont(pdt.font0)
        self.ql_text_start.setAlignment(Qt.AlignCenter)
        self.ql_text_menu.setAlignment(Qt.AlignCenter)
        self.ql_text_choice_vocab.setAlignment(Qt.AlignCenter)
        self.ql_text_setting.setAlignment(Qt.AlignCenter)
        self.ql_text_popup.setAlignment(Qt.AlignCenter)
        self.ql_text_detail.setAlignment(Qt.AlignCenter)
        self.ql_text_end.setAlignment(Qt.AlignCenter)

        # 创建垂直布局，并添加所有标签
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

        self.qvbl.addWidget(self.ql_text_start)
        self.qvbl.addWidget(self.ql_img_menu)
        self.qvbl.addWidget(self.ql_text_menu)
        self.qvbl.addWidget(self.ql_text_choice_vocab)
        self.qvbl.addWidget(self.ql_img_setting)
        self.qvbl.addWidget(self.ql_text_setting)
        self.qvbl.addWidget(self.ql_img_popup)
        self.qvbl.addWidget(self.ql_text_popup)
        self.qvbl.addWidget(self.ql_img_detail)
        self.qvbl.addWidget(self.ql_text_detail)
        self.qvbl.addWidget(self.ql_text_end)

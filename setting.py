# coding:utf-8
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QSpinBox, QPushButton, QCheckBox, QVBoxLayout, QGridLayout
import WordsBoomPlus.public_data as pdt


# 设置界面类
class Setting(QDialog):
    def __init__(self):
        super(Setting, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("设置")
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

        # 创建界面上的各个控件
        self.ql_popup_cycle = QLabel("弹窗周期(分钟)")
        self.qsb_popup_cycle = QSpinBox()
        self.ql_words_per_popup = QLabel("每组单词数")
        self.qsb_words_per_popup = QSpinBox()
        self.ql_rounds_per_word = QLabel("每组记忆轮数")
        self.qsb_rounds_per_word = QSpinBox()
        self.qpb_learning_mode = QPushButton("切换学习模式")
        self.ql_learning_mode = QLabel()
        self.qcb_confirm_complete = QCheckBox("完全认识防误操作")
        self.qcb_confirm_delete = QCheckBox("取消收藏防误操作")
        self.qcb_right_sound = QCheckBox("正确音效")
        self.qcb_wrong_sound = QCheckBox("错误音效")

        # 设置各个控件的字体和布局
        self.qgl = QGridLayout()
        self.qvbl = QVBoxLayout(self)
        self.ql_popup_cycle.setFont(pdt.font0)
        self.qsb_popup_cycle.setFont(pdt.font0)
        self.qsb_popup_cycle.setMinimum(1)
        self.qsb_popup_cycle.setMaximum(360)
        self.ql_words_per_popup.setFont(pdt.font0)
        self.qsb_words_per_popup.setFont(pdt.font0)
        self.qsb_words_per_popup.setMinimum(1)
        self.qsb_words_per_popup.setMaximum(100)
        self.ql_rounds_per_word.setFont(pdt.font0)
        self.qsb_rounds_per_word.setFont(pdt.font0)
        self.qsb_rounds_per_word.setMinimum(1)
        self.qsb_rounds_per_word.setMaximum(10)
        self.qpb_learning_mode.setFont(pdt.font0)
        self.ql_learning_mode.setFont(pdt.font0)
        self.qcb_confirm_complete.setFont(pdt.font0)
        self.qcb_confirm_delete.setFont(pdt.font0)
        self.qcb_right_sound.setFont(pdt.font0)
        self.qcb_wrong_sound.setFont(pdt.font0)
        self.qgl.addWidget(self.ql_popup_cycle, 0, 0)
        self.qgl.addWidget(self.qsb_popup_cycle, 0, 1)
        self.qgl.addWidget(self.ql_words_per_popup, 1, 0)
        self.qgl.addWidget(self.qsb_words_per_popup, 1, 1)
        self.qgl.addWidget(self.ql_rounds_per_word, 2, 0)
        self.qgl.addWidget(self.qsb_rounds_per_word, 2, 1)
        self.qgl.addWidget(self.qpb_learning_mode, 3, 0)
        self.qgl.addWidget(self.ql_learning_mode, 3, 1)
        self.qvbl.addLayout(self.qgl)
        self.qvbl.addWidget(self.qcb_confirm_complete)
        self.qvbl.addWidget(self.qcb_confirm_delete)
        self.qvbl.addWidget(self.qcb_right_sound)
        self.qvbl.addWidget(self.qcb_wrong_sound)

        # 设置默认值
        self.set_setting()

        # 信号与槽连接
        self.qpb_learning_mode.clicked.connect(self.change_learning_mode)

        # 调整窗口大小并固定大小
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # 设置值
    def set_setting(self):
        # 从数据中获取设置值并设置到控件上
        self.qsb_popup_cycle.setValue(pdt.setting['popup_cycle'])
        self.qsb_words_per_popup.setValue(pdt.setting['words_per_popup'])
        self.qsb_rounds_per_word.setValue(pdt.setting['rounds_per_word'])
        if pdt.setting['learning_mode']:
            self.ql_learning_mode.setText('显示英文\n回忆中文')
        else:
            self.ql_learning_mode.setText('显示中文\n回忆英文')
        self.qcb_confirm_complete.setChecked(pdt.setting['confirm_complete'])
        self.qcb_confirm_delete.setChecked(pdt.setting['confirm_delete'])
        self.qcb_right_sound.setChecked(pdt.setting['right_sound'])
        self.qcb_wrong_sound.setChecked(pdt.setting['wrong_sound'])

    # 切换学习模式
    def change_learning_mode(self):
        # 根据当前文本内容判断当前模式并切换显示文本
        if self.ql_learning_mode.text() == '显示中文\n回忆英文':
            self.ql_learning_mode.setText('显示英文\n回忆中文')
        else:
            self.ql_learning_mode.setText('显示中文\n回忆英文')

    # 关闭窗口事件处理
    def closeEvent(self, event):
        # 将控件上的设置值保存到数据中并保存到json文件中
        pdt.setting['popup_cycle'] = self.qsb_popup_cycle.value()
        pdt.setting['words_per_popup'] = self.qsb_words_per_popup.value()
        pdt.setting['rounds_per_word'] = self.qsb_rounds_per_word.value()
        if self.ql_learning_mode.text() == '显示中文\n回忆英文':
            pdt.setting['learning_mode'] = 0
        else:
            pdt.setting['learning_mode'] = 1
        pdt.setting['confirm_complete'] = self.qcb_confirm_complete.isChecked()
        pdt.setting['confirm_delete'] = self.qcb_confirm_delete.isChecked()
        pdt.setting['right_sound'] = self.qcb_right_sound.isChecked()
        pdt.setting['wrong_sound'] = self.qcb_wrong_sound.isChecked()
        with open('setting.json', 'w', encoding='utf-8') as f:
            json.dump(pdt.setting, f)

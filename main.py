# coding:utf-8
import json
import msvcrt
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMessageBox
import public_data as pdt
from login import Login
from waiting import Waiting


# 文件锁，防止多开
def checkSingleProcess():
    global PIDFILE
    try:
        PIDFILE = open('myapp.lock', "r")  # 获取运行的文件路径
        msvcrt.locking(PIDFILE.fileno(), msvcrt.LK_NBLCK, 1)  # 尝试以非阻塞方式锁定文件
    except IOError:
        # 如果文件已被锁定，表示程序已在运行
        return False
    return True


if __name__ == '__main__':
    PIDFILE = None  # 初始化 PIDFILE
    app = QApplication(sys.argv)

    # 从 JSON 文件中读取设置信息并存储到全局变量中
    with open('setting.json', encoding='utf-8') as f:
        pdt.setting = json.load(f)

    if not os.path.exists("audio"):
        os.mkdir("audio")
    pdt.icon = QIcon('img/icon.png')
    pdt.font0 = QFont()
    pdt.font0.setPointSize(16)
    pdt.font1 = QFont()
    pdt.font1.setPointSize(9)
    pdt.font2 = QFont()
    pdt.font2.setPointSize(20)
    pdt.font2.setBold(True)
    pdt.player = QMediaPlayer()
    pdt.waiting = Waiting()

    # 防止多开
    if not checkSingleProcess():
        msg = QMessageBox()
        msg.setWindowIcon(pdt.icon)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('警告')
        msg.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面
        msg.setText('单词弹弹弹已经在运行！')
        msg.exec_()
        sys.exit()

    # 初始化应用程序
    app.setQuitOnLastWindowClosed(False)  # 窗口关闭时不退出应用程序
    pdt.login = Login()
    pdt.login.show()
    sys.exit(app.exec_())  # 运行应用程序并进入事件循环

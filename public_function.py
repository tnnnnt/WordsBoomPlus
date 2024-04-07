# coding:utf-8
import asyncio
import os
import requests
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtWidgets import QMessageBox
import WordsBoomPlus.public_data as pdt
from WordsBoomPlus import asyncio_c


# 检查密码是否符合要求
def check_password(password):
    return 6 <= len(password) <= 16


# 检查手机号格式是否规范
def check_phone(phone):
    return len(phone) == 11 and phone[0] == '1' and phone[1] > '2'


# 检查验证码格式是否规范
def check_code_format(code):
    if len(code) != 6:
        return False
    for i in code:
        if i not in '0123456789':
            return False
    return True


# 修改收藏状态
def change_collection_state(w, favorite, favor_icon, word, chinese):
    if favorite == 1 and favor_icon == "img/unfavorited.png":
        asyncio.run(asyncio_c.set_collection(pdt.phone, word))
        del pdt.menu.collect_words.words_map[word]
        pdt.menu.collect_words.words_map[word].close()
        return 0
    elif favorite == 0 and favor_icon == "img/favorited.png":
        if asyncio.run(asyncio_c.has_space_in_collections(pdt.phone)):
            asyncio.run(asyncio_c.set_collection(pdt.phone, word))
            pdt.menu.collect_words.add_word(word, chinese)
            return 1
        else:
            QMessageBox.information(w, "提示", "收藏夹已满, 请先删除一些单词或进行充值")
            return 0
    return favorite


# 播放单词发音
def audio_play(word, type):
    wav_path = "audio/" + word + "_" + type + ".wav"
    if not os.path.exists(wav_path):
        # 如果本地不存在该单词的发音文件，则从网络下载
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
        stream_url = "https://dict.youdao.com/dictvoice?audio=" + word + "&type=" + type
        response = requests.get(stream_url, headers=headers)
        with open(wav_path, "wb") as f:
            f.write(response.content)
    # 播放单词发音
    pdt.player.setMedia(QMediaContent(QUrl.fromLocalFile(wav_path)))
    pdt.player.play()

# coding:utf-8
import asyncio
from decimal import Decimal
import datetime

IP = '123.175.77.65'  # 服务器的IP地址
PORT = 11451  # 服务器监听的端口号
BUFLEN = 8192  # 一次最多读取的字节数


# 异步函数，向服务器发送请求并接收响应
async def req(s):
    reader, writer = await asyncio.open_connection(IP, PORT)  # 连接到服务器
    writer.write(s.encode())  # 发送消息给服务器
    await writer.drain()  # 等待接收来自服务器的响应
    data = await reader.read(BUFLEN)  # 从服务器接收数据（每次最多读取BUFLEN个字节）
    ret = data.decode()
    writer.close()
    await writer.wait_closed()
    return ret


# 检查手机号是否存在
async def check_phone_exist(phone):
    return await req('00' + phone) == '1'


# 接收验证码
async def receive_code(phone):
    return await req('01' + phone) == '1'


# 检查验证码
async def check_code(phone, code):
    return await req('02' + phone + code) == '1'


# 添加用户
async def add_user(phone, password):
    await req('03' + phone + password)


# 修改密码次数
async def modify_password_times(phone):
    return await req('04' + phone) == '1'


# 修改密码
async def change_password(phone, password):
    return await req('05' + phone + password) == '1'


# 检查密码
async def check_password(phone, password):
    return await req('06' + phone + password) == '1'


# 获取注册时间
async def get_reg_time(phone):
    return await req('07' + phone)


# 获取昵称
async def get_nickname(phone):
    return await req('08' + phone)


# 获取头像编号
async def get_avatar_num(phone):
    return await req('09' + phone)


# 修改头像编号
async def change_avatar_num(phone, n):
    await req('10' + phone + str(n))


# 修改昵称
async def change_nickname(phone, nickname):
    await req('11' + phone + nickname)


# 销毁账户
async def destroy_account(phone):
    await req('12' + phone)


# 修改手机次数
async def modify_phone_times(phone):
    return await req('13' + phone) == '1'


# 更换手机号
async def change_phone(phone, new_phone):
    return await req('14' + phone + new_phone) == '1'


# 重置词书权重
async def reset_w(phone, vocab):
    await req('15' + phone + vocab)


# 获取中文和收藏状态
async def get_chinese_and_collection(phone, word):
    return eval(await req('16' + phone + word))


# 设置单词权重
async def set_w(phone, word, change_w):
    await req('17' + phone + word + change_w)


# 收藏单词
async def set_collection(phone, word):
    await req('18' + phone + word)


# 获取词库的所有单词
async def get_words(phone, vocab, words_per_popup):
    return eval(await req('19' + phone + vocab + ',' + str(words_per_popup)))


# 检测是否有收藏空间
async def has_space_in_collections(phone):
    return await req('20' + phone) == '1'


# 检查单词是否存在
async def check_word_exist(word):
    return await req('21' + word) == '1'


# 获取例句
async def get_example_sentences(word):
    return eval(await req('22' + word))


# 获取助记
async def get_mnemonic(word):
    return eval(await req('23' + word))


# 获取个人助记
async def get_personal_mnemonic(phone, word):
    return await req('24' + phone + word)


# 设置助记
async def set_mnemonic(phone, word, mnemonic):
    await req('25' + phone + word + ',' + mnemonic)


# 获取收藏单词
async def get_collection_words(phone):
    return eval(await req('26' + phone))


# 获取词汇量
async def get_vocabulary(phone):
    return int(await req('27' + phone))


# 获取单词和中文
async def get_words_and_chinese_s():
    return eval(await req('28'))


# 获取错误的中文
async def get_wrong_chinese_s(word):
    a = eval(await req('29' + word))
    ret = []
    for i in a:
        ret.append(i[0])
    return ret


# 设置词汇量
async def set_vocabulary(phone, n):
    await req('30' + phone + str(n))


# 获取词汇量排名
async def get_vocabulary_rank():
    return eval(await req('31'))


# 获取助记排名
async def get_mnemonic_rank():
    return eval(await req('32'))


# 获取个人词汇量排名
async def get_personal_vocabulary_rank(phone):
    return await req('33'+phone)


# 获取个人助记排名
async def get_personal_mnemonic_rank(phone):
    return eval(await req('34'+phone))


# 发送反馈
async def send_feedback(phone, feedback):
    await req('35'+phone+feedback)


# 获取邮件
async def get_emails(phone):
    return eval(await req('36'+phone))


# 删除邮件
async def del_email(id):
    await req('37'+str(id))


# 获取最新版本号
async def get_new_version():
    return await req('38')

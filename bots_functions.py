import requests
import datetime
import random
import time


# Отвечает стикеров на отправленный стикер.
# send - айди стикера, который отправил пользователь
# reply - айди стикера, который отправил бот
def reply_sticker(bot, send=163, reply=19133):
    try:
        if send == bot.event.message['attachments'][0]['sticker']['sticker_id']:
            bot.write_msg('', dop_dict={"sticker_id": reply})
    except:
        pass


def get_token():
    with open('token.txt', 'r') as f:
        token = f.read()
    return token


# У нас в вузе одна неделя Знаменатель, другая Числитель, иногда это требуется знать, от этого зависит наше расписание
def bot_week():
    # На хостинге время UTC+0, поэтому приходится прибавлять 5 часов
    now = datetime.datetime.now() + datetime.timedelta(hours=+5)
    week = datetime.datetime.isocalendar(now)[1]  # узнать номер недели
    if week % 2 == 0:
        message = "Знаменатель"
    else:
        message = "Числитель"
    return message


def show_help():
    help_text = 'Доступные команды:\n'
    help_text += '\n[Бот неделя]: показываю тип недели (Знаменатель\\Числитель)'
    help_text += '\n[Вадим.]: злюся на вадима'
    help_text += '\n[*Стикер ореха*]: отправляю стикер'
    return help_text


# пока безполезная функция, которая печатает ошибку и записывает в логи время переподключения
def reconnect(e):
    with open("log.log", 'a+', encoding='utf-8') as f:
        f.write("переподключение " + str(datetime.datetime.now() + datetime.timedelta(hours=5)) + '\n')
    print(e)
    time.sleep(3)


class VkBotMessages:
    def __init__(self, vk, event):
        self.vk = vk
        self.event = event
        if event.from_chat:
            self.from_type = 'chat_id'
            self.chat_id = event.chat_id
            self.user_id = event.message['from_id']
        else:
            self.from_type = 'user_id'
            self.chat_id = event.message['from_id']
            self.user_id = self.chat_id

    def write_msg(self, message, dop_dict=None):
        vk_args = {self.from_type: self.chat_id, "message": message, 'random_id': random.randint(0, 2048)}
        if dop_dict:
            vk_args.update(dop_dict)
        self.vk.method('messages.send', vk_args)

    def kick(self, user_id):
        if self.event.from_chat:
            vk_args = {"chat_id": self.chat_id, "user_id": user_id}
            self.vk.method('messages.removeChatUser', vk_args)


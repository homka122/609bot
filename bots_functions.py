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
        f.write((datetime.datetime.now() + datetime.timedelta(hours=5)).strftime("[%Y/%m/%d: %H:%M:%S] ") + str(e) + '\n')
    print(e)
    time.sleep(1)


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

    def get_full_name(self, dop_dict=None):
        vk_args = {'user_ids': [self.user_id]}
        if dop_dict:
            vk_args.update(dop_dict)
        result = self.vk.method('users.get', vk_args)
        return result[0]['first_name'] + " " + result[0]['last_name']

    def wake_up_guys(self, text):
        name = self.get_full_name(dop_dict={'name_case': "ins"})
        text = text.split(" ", 1)
        if len(text) > 1:
            cmd, mes = text
        else:
            cmd = text[0]
            mes = ""
        first_group = '281914353 278609920 168827694 255416426 155996138' \
                      ' 463908361 251018870 454286695 213785297 187510320 205682553'
        second_group = '202803940 244359487 608305868 318556720 180488860 237545860 ' \
                       '58485102 612990907 218436496 214561873 137407116'
        first_subgroup = '281914353 278609920 168827694 255416426 155996138 463908361 251018870 454286695'
        second_subgroup = '213785297 187510320 205682553 202803940 244359487 608305868 318556720'
        third_subgroup = '180488860 237545860 58485102 612990907 218436496 214561873 137407116'
        hamsters = '380679686'
        choice = {"@1гр": first_group, "@2гр": second_group, "@1подгр": first_subgroup,
                  "@2подгр": second_subgroup, "@3подгр": third_subgroup, "@хомяки": hamsters}
        guys = ''
        for guy in choice[cmd].split():
            guys += f"@id{guy} (.) "
        self.write_msg(f"{mes} (Создано: {name}) [ {guys} ]")

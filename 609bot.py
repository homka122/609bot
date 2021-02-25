import requests
import datetime, random
import time
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def write_msg(user_id, message, vk, chat_id='user_id'):
    vk.method('messages.send', {
        chat_id: user_id,
        "message": message,
        'random_id': random.randint(0, 2048)
    })


def bot_week():
    now = datetime.datetime.now() + datetime.timedelta(hours=+5)
    week = datetime.datetime.isocalendar(now)[1]
    if week % 2 == 0:
        message = "Знаменатель"
    else:
        message = "Числитель"
    return message


def angry_vadim():
    return "вадим😡😡😡"


def show_help():
    help = 'Доступные команды:\n'
    help += '\nБот неделя: показывает день недели'
    return help


with open('token.txt', 'r') as f:
    token = f.read()

vk = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk, group_id=202842010)

now = datetime.datetime.now() + datetime.timedelta(hours=5)
print(now)
print(datetime.date.isocalendar(now))

try:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_chat:
                chat_id = 'chat_id'
                user_id = event.chat_id
                from_id = event.message['from_id']
            else:
                chat_id = 'user_id'
                user_id = event.message['from_id']
                from_id = event.message['from_id']
            text = event.message['text'].lower()
            if text.lower() == "бот неделя":
                write_msg(user_id, bot_week(), vk, chat_id)
            if text.lower() == "вадим." and from_id == 380679686:
                write_msg(user_id, angry_vadim(), vk, chat_id)
            if text.lower() == 'бот хелп':
                write_msg(user_id, show_help(), vk, chat_id)
except requests.exceptions.ReadTimeout:
    print("переподключение" + str(datetime.datetime.now() + datetime.timedelta(hours=5)))
    time.sleep(3)

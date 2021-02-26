import requests
import datetime, random


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


class VkBot:
    def __init__(self, vk):
        self.vk = vk

    def write_msg(self, from_id, message, from_type='user_id'):
        self.vk.method('messages.send', {
            from_type: from_id,
            "message": message,
            'random_id': random.randint(0, 2048)
        })

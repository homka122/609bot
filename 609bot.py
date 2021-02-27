import requests
import time, random
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from bots_functions import *

with open('token.txt', 'r') as f:
    token = f.read()

vk = vk_api.VkApi(token=token)
VkBot = VkBot(vk)
longpoll = VkBotLongPoll(vk, group_id=202842010)

while True:
    try:
        print('подключение')
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_chat:
                    from_type = 'chat_id'
                    chat_id = event.chat_id
                    user_id = event.message['from_id']
                else:
                    from_type = 'user_id'
                    chat_id = event.message['from_id']
                    user_id = chat_id
                text = event.message['text'].lower()
                # 'attachments': [{'type': 'sticker', 'sticker': {'product_id': 4, 'sticker_id': 163
                if event.message['attachments']:
                    if event.message['attachments'][0]['type'] == 'sticker':
                        if event.message['attachments'][0]['sticker']['sticker_id'] == 163:
                            vk.method('messages.send', {
                                'sticker_id': 19133,
                                from_type: chat_id,
                                'message': 'орех',
                                'random_id': random.randint(0, 2048)
                            })
                if text == "бот неделя":
                    VkBot.write_msg(chat_id, bot_week(), from_type)
                if text == "вадим.":
                    VkBot.write_msg(chat_id, angry_vadim(), from_type)
                if text == 'бот хелп':
                    VkBot.write_msg(chat_id, show_help(), from_type)
    except requests:
        with open("log.log", 'a+', encoding='utf-8') as f:
            f.write("переподключение " + str(datetime.datetime.now() + datetime.timedelta(hours=5)) + '\n')
        time.sleep(3)

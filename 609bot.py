import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from bots_functions import *

token = get_token()
vk = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk, group_id=202842010)

while True:
    try:
        print('подключение')
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                VkBot = VkBotMessages(vk, event)
                reply_sticker(VkBot)

                text = event.message['text'].lower()
                if text == "бот неделя":
                    VkBot.write_msg(bot_week())
                if text == "вадим.":
                    VkBot.write_msg("вадим😡😡😡")
                    # VkBot.kick(249198867)
                if text == 'бот хелп':
                    VkBot.write_msg(show_help())
    except Exception as e:
        reconnect(e)

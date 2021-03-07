import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from bots_functions import *
import NewGroup
from config import TOKEN, GROUP_ID
import json

vk = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk, group_id=GROUP_ID)
DEBUG = 0


def main():
    print('подключение')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.message['from_id'] > 0:
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
            if text == 'info':
                VkBot.write_msg(NewGroup.info())
            try:
                if text.split()[0] in ["@1гр", "@2гр", "@1подгр", "@2подгр", "@3подгр", "@хомяки"]:
                    VkBot.wake_up_guys(text)
            except:
                pass


if not DEBUG:
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Бот остановлен")
            break
        except Exception as e:
            reconnect(e)
else:
    main()
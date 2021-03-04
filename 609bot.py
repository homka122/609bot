import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from bots_functions import *
from NewGroup import new_group
import json

token = get_token()
vk = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk, group_id=202842010)
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
            try:
                if text.split()[0] == "нгру":
                    if event.from_user:
                        result = new_group(VkBot, text)
                        if result:
                            with open("homka.json", 'w', encoding='UTF-8') as f:
                                json.dump(result, f, ensure_ascii=False, indent=2)
                    else:
                        VkBot.write_msg("Эти команды отныне доступны лишь в лс")
                if text.split()[0] in ["@1гр", "@2гр", "@1подгр", "@2подгр", "@3подгр", "@хомяки"]:
                    VkBot.wake_up_guys(text)
            except:
                pass


if not DEBUG:
    while True:
        try:
            main()
        except Exception as e:
            reconnect(e)
else:
    main()
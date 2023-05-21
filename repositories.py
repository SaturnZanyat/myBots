import json
import re

import aiohttp
from telebot import types
import configparser

async def get_random_quest():
    config = configparser.ConfigParser()
    config.read("setting.ini")
    async with aiohttp.ClientSession() as session:
        async with session.get(config["Django"]["api_quest"]) as response:
            return await response.json()

async def add_static_kb():
    a1 = types.InlineKeyboardButton(str("Старт"), callback_data=str("/start"))
    a2 = types.InlineKeyboardButton(str("Помощь"), callback_data=str("/help"))
    a3 = types.InlineKeyboardButton(str("Квиз"), callback_data=str("/give_number"))
    a4 = types.InlineKeyboardButton(str("Купить"), callback_data=str("/buy"))
    answer_kb = types.ReplyKeyboardMarkup()
    answer_kb.add(a1,a2,a3,a4)
    return answer_kb

async def add_answer_kb(a1,a2,a3):
    a1 = types.InlineKeyboardButton(str(a1), callback_data=str(a1))
    a2 = types.InlineKeyboardButton(str(a2), callback_data=str(a2))
    a3 = types.InlineKeyboardButton(str(a3), callback_data=str(a3))
    answer_kb = types.InlineKeyboardMarkup()
    answer_kb.add(a1,a2,a3)
    return answer_kb

async def validate_number(number):
    pattern = "\D"
    matter = re.findall(pattern, number)
    if not matter:
        return number
    else:
        return False

async def check_correct_number(answ, number):
    if number == answ:
        return True
    else:
        return False

async def register_button_pick(call):
    return call

async def get_answer(request, chat_id, field: str):
    with open("clients.json", "r") as ff:
        data_from_json = json.load(ff)
    data_from_json[chat_id] = {"{0}".format(field): request}
    with open("clients.json", "w") as ff:
        json.dump(data_from_json, ff, indent=4, ensure_ascii=False)
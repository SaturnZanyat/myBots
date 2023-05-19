import json
import re
import configparser

import telebot
from telebot import types
from telebot.types import Message

# class MyBot:
#
#     def __init__(self) -> None:
#         super().__init__()

config = configparser.ConfigParser()
config.read("setting.ini")
token = config["Bot"]["bot"]
payment_token = config["Bot"]["payment"]
PRICE = types.LabeledPrice(label="Звезда смерти", amount=int(config["Price"]["zvezda"])*100)  # в копейках (руб)
bot = telebot.TeleBot(token)

def validate_number(number):
    pattern = "\D"
    matter = re.findall(pattern, number)
    if not matter:
        return number
    else:
        return False

def check_correct_number(answ, number):
    if number == answ:
        return True
    else:
        return False

def handler_number(message: Message):
    chat_id = message.chat.id
    request = message.text
    if validate_number(request):
        with open("clients.json", "r") as ff:
            data_from_json = json.load(ff)
        data_from_json[chat_id] = {"number": request}
        mes = "Ваш ответ принят: " + request
        with open("clients.json", "w") as ff:
            json.dump(data_from_json, ff, indent=4, ensure_ascii=False)
    else:
        mes = "Ответ написан с ошибкой. Напишите ответ без пробелов и сторонних символов. Сейчас он выглядит так: " + request
    correct_num = 13
    if check_correct_number(correct_num, int(request)):
        mes = mes + " Вы посчитали правильно!"
    else:
        mes = mes + " К сожалению, вы ошиблись. Правильный ответ был {0}. У гусеницы {0} ножек.".format(correct_num)
    bot.send_message(chat_id, mes)
    bot.send_message(chat_id, "Вопрос 2. Сколько птиц пролетело за окном. Введите ваш ответ: ")
    bot.register_next_step_handler(message, callback=handler_bird)

def handler_bird(message: Message):
    chat_id = message.chat.id
    request = message.text
    if validate_number(request):
        with open("clients.json", "r") as ff:
            data_from_json = json.load(ff)
        data_from_json[chat_id] = {"bird": request}
        mes = "Ваш ответ принят: " + request
        with open("clients.json", "w") as ff:
            json.dump(data_from_json, ff, indent=4, ensure_ascii=False)
    else:
        mes = "Ответ написан с ошибкой. Напишите ответ без пробелов и сторонних символов. Сейчас он выглядит так: " + request
    correct_bird = 6
    if check_correct_number(correct_bird, int(request)):
        mes = mes + " Вы посчитали правильно!"
    else:
        mes = mes + " К сожалению, вы ошиблись. Правильный ответ был {0}. За окном было {0} птиц.".format(correct_bird)
    bot.send_message(chat_id, mes)

@bot.message_handler(commands=["give_number"])
def send_number(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Вопрос 1. Посчитайте, пожалуйста, сколько ножек у гусениц. Введите свой ответ: ")
    bot.register_next_step_handler(message, callback=handler_number)


@bot.message_handler(commands=["buy"])
def buy(message: Message):
    if payment_token.split(':')[1] == 'TEST':
        bot.send_message(message.chat.id, "Тестовый платеж!!!")

    bot.send_invoice(message.chat.id,
                           title="Покупка Звезды Смерти",
                           description="Абсолютно новая Здезда Смерти",
                           provider_token=payment_token,
                           currency="rub",
                           # photo_url="",
                           # photo_width=416,
                           # photo_height=234,
                           # photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="buy_zvezda",
                           invoice_payload="test-invoice-payload")

@bot.message_handler(content_types=["text"])
def start(message: Message):
    chat_id = message.chat.id
    request = message.text
    if request == '/start':
        response = "Здравствуйте. Этот бот может провести небольшой опрос. Для того, чтобы начать введите '/give_number'"
    elif request == '/help':
        response = "Это тестовый бот с ограниченным функционалом"
    else:
        response = "Извините, бот вас не понял"
    bot.send_message(chat_id, response)

bot.polling(non_stop=True, interval=0)
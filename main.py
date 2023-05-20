import asyncio
import configparser
import json
import re

from telebot import types, asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.types import Message
from telebot.asyncio_handler_backends import State, StatesGroup

from DB import connect_DB, close_connection_DB
from repositories import validate_number, check_correct_number, get_answer

config = configparser.ConfigParser()
config.read("setting.ini")
token = config["Bot"]["bot"]
payment_token = config["Bot"]["payment"]
PRICE = types.LabeledPrice(label="Звезда смерти", amount=int(config["Price"]["zvezda"])*100)  # в копейках (руб)
bot = AsyncTeleBot(token, state_storage=StateMemoryStorage())

class MyStates(StatesGroup):
    start = State() # statesgroup should contain states
    number = State()
    bird = State()
    buy = State()

connection = connect_DB()

@bot.message_handler(commands=["buy"])
async def buy(message: Message):
    if payment_token.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж!!!")

    await bot.send_invoice(message.chat.id,
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

@bot.message_handler(state=MyStates.number)
async def handler_number(message: Message):
    correct_num = 13
    chat_id = message.chat.id
    request = message.text
    if await validate_number(request):
        await get_answer(request, chat_id, "number")
        mes = "Ваш ответ принят: " + request
    else:
        mes = "Ответ написан с ошибкой. Напишите ответ без пробелов и сторонних символов. Сейчас он выглядит так: " + request
    if await check_correct_number(correct_num, int(request)):
        mes = mes + " Вы посчитали правильно!"
    else:
        mes = mes + " К сожалению, вы ошиблись. Правильный ответ был {0}. У гусеницы {0} ножек.".format(correct_num)
    await bot.set_state(message.from_user.id, MyStates.bird, chat_id)
    await bot.send_message(chat_id, mes)
    await bot.send_message(chat_id, "Вопрос 2. Сколько птиц пролетело за окном. Введите ваш ответ: ")
    # await bot.register_next_step_handler(message, callback=self.handler_bird)

@bot.message_handler(state=MyStates.bird)
async def handler_bird(message: Message):
    chat_id = message.chat.id
    request = message.text
    correct_bird = 6
    if await validate_number(request):
        await get_answer(request, chat_id, "bird")
        mes = "Ваш ответ принят: " + request
    else:
        mes = "Ответ написан с ошибкой. Напишите ответ без пробелов и сторонних символов. Сейчас он выглядит так: " + request
    if await check_correct_number(correct_bird, int(request)):
        mes = mes + " Вы посчитали правильно!"
    else:
        mes = mes + " К сожалению, вы ошиблись. Правильный ответ был {0}. За окном было {0} птиц.".format(correct_bird)
    await bot.send_message(chat_id, mes)

@bot.message_handler(commands=["give_number"])
async def send_number(message: Message):
    chat_id = message.chat.id
    await bot.set_state(message.from_user.id, MyStates.number, chat_id)
    await bot.send_message(chat_id, "Вопрос 1. Посчитайте, пожалуйста, сколько ножек у гусениц. Введите свой ответ: ")

@bot.message_handler(content_types=["text"])
async def start(message: Message):
    chat_id = message.chat.id
    request = message.text
    user_id = message.from_user.id
    if request == '/start':
        response = "Здравствуйте. Этот бот может провести небольшой опрос. Для того, чтобы начать введите '/give_number'"
    elif request == '/help':
        response = "Это тестовый бот с ограниченным функционалом"
    # elif request == '/buy':
    #     await bot.set_state(user_id, MyStates.buy, chat_id)
    #     response = "Вы перенаправляетесь в 'покупки'. Доступные лоты: {0}".format(PRICE.label)
    else:
        response = "Извините, бот вас не понял"
    await bot.set_state(user_id, MyStates.start, chat_id)
    await bot.send_message(chat_id, response)

while True:
    try:
        bot.add_custom_filter(asyncio_filters.StateFilter(bot))
        bot.add_custom_filter(asyncio_filters.IsDigitFilter())

        asyncio.run(bot.polling(non_stop=True, interval=0))
        close_connection_DB(connection)
    except Exception as err:
        print("!!!!!!! Ошибка: ", err)
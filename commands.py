import configparser

from telebot import types, asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.types import Message, CallbackQuery
from telebot.asyncio_handler_backends import State, StatesGroup

from DB import connect_DB
from repositories import validate_number, check_correct_number, get_answer, add_answer_kb, get_random_quest, \
    add_static_kb, make_answer_kb

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
    put_answer = State()

connection = connect_DB()


@bot.message_handler(commands=["start", "help"])
async def start(message: Message):
    chat_id = message.chat.id
    request = message.text
    user_id = message.from_user.id
    # kb = await add_static_kb()
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Сайт Хабр", url='https://habr.com/ru/all/')
    button2 = types.InlineKeyboardButton("Наша техническая поддержка", url='https://habr.com/ru/docs/help/rules/')
    if request == '/start':
        markup.add(button1)
        await bot.send_message(message.chat.id,
                         "Этот бот представляет компанию "
                         "*Здесь могло бы быть имя вашей компании*",
                         reply_markup=markup)
    elif request == '/help':
        markup.add(button2)
        await bot.send_message(message.chat.id,
                               "Бот обладает ограниченным функционалом. Вы можете ознакомиться с help-страницей"
                               "на сайте",
                               reply_markup=markup)
    else:
        await bot.send_message(message.chat.id,
                               "Бот вас не понял")
    await bot.set_state(user_id, MyStates.start, chat_id)


@bot.message_handler(commands=["buy"])
async def buy(message: Message):
    if payment_token.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж!!!")

    await bot.send_invoice(message.chat.id,
                           title="Покупка Звезды Смерти",
                           description="Абсолютно новая Здезда Смерти",
                           provider_token=payment_token,
                           currency="rub",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="buy_zvezda",
                           invoice_payload="test-invoice-payload")

@bot.message_handler(commands=["give_number"])
async def send_number(message: Message):
    chat_id = message.chat.id
    quest = await get_random_quest()
    await bot.set_state(message.from_user.id, MyStates.put_answer, chat_id)
    async with bot.retrieve_data(message.from_user.id, chat_id) as data:
        data['step'] = 1
        data['answer'] = quest.get('answer')
        data['quest'] = quest.get('quest')
        markup = await make_answer_kb(int(data['answer']))
        await bot.send_message(chat_id, "Вопрос {0}. {1} ".format(data['step'], data['quest']), reply_markup=markup)

@bot.callback_query_handler(func=None, state=MyStates.put_answer)
async def button_click_an(query: CallbackQuery):
    await bot.answer_callback_query(query.id)
    answer = query.data
    await bot.set_state(query.from_user.id, MyStates.start)
    async with bot.retrieve_data(query.from_user.id) as data:
        correct = data.get('answer')
        if answer == correct:
            data['step'] += 1
            if data['step'] > 3:
                await bot.send_message(query.from_user.id, "Вы молодец!")
            else:
                quest = await get_random_quest()
                data['answer'] = quest.get('answer')
                data['quest'] = quest.get('quest')
                markup = await make_answer_kb(data['answer'])
                await bot.set_state(query.from_user.id, MyStates.put_answer)
                await bot.send_message(query.from_user.id, "Вы ответили верно. Вопрос {0}. {1} ".format(data['step'], data['quest']), reply_markup=markup)
        else:
            await bot.send_message(query.from_user.id, "Вы проиграли. Вы ответили неверно. Ответом было число {0}".format(correct))
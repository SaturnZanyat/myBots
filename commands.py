import configparser

from telebot import types, asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.types import Message, CallbackQuery
from telebot.asyncio_handler_backends import State, StatesGroup

from DB import connect_DB
from repositories import validate_number, check_correct_number, get_answer, add_answer_kb, get_random_quest

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
    # await bot.send_message(chat_id, response)


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


@bot.message_handler(state=MyStates.bird)
async def handler_bird(message: Message):
    chat_id = message.chat.id
    request = message.text
    correct_bird = 6
    if await validate_number(request):
        await get_answer(request, chat_id, "bird")
        mes = "Ваш ответ принят: {0}".format(request)
    else:
        mes = "Ответ написан с ошибкой. Напишите ответ без пробелов и сторонних символов. Сейчас он выглядит так: {0}".format(request)
    if await check_correct_number(correct_bird, int(request)):
        mes = "{0} Вы посчитали правильно!".format(mes)
    else:
        mes = "{0} К сожалению, вы ошиблись. Правильный ответ был {1}. За окном было {1} птиц.".format(mes, correct_bird)
    await bot.send_message(chat_id, mes)

@bot.message_handler(commands=["give_number"])
async def send_number(message: Message):
    markup = await add_answer_kb(18,13,6)
    chat_id = message.chat.id
    quest = await get_random_quest()
    await bot.set_state(message.from_user.id, MyStates.put_answer, chat_id)
    async with bot.retrieve_data(message.from_user.id, chat_id) as data:
        data['step'] = 1
        data['answer'] = quest.get('answer')
        data['quest'] = quest.get('quest')
        await bot.send_message(chat_id, "Вопрос {0}. {1} ".format(data['step'], data['quest']), reply_markup=markup)

@bot.callback_query_handler(func=None, state=MyStates.put_answer)
async def button_click_an(query: CallbackQuery):
    await bot.answer_callback_query(query.id)
    answer = query.data
    await bot.set_state(query.from_user.id, MyStates.start)
    async with bot.retrieve_data(query.from_user.id) as data:
        print(data)
        correct = data.get('answer')
        if answer == correct:
            data['step'] += 1
            if data['step'] > 3:
                await bot.send_message(query.from_user.id, "Вы молодец!")
            else:
                quest = await get_random_quest()
                data['answer'] = quest.get('answer')
                data['quest'] = quest.get('quest')
                markup = await add_answer_kb(18, 13, 6) #TODO: берётся из бэка
                await bot.set_state(query.from_user.id, MyStates.put_answer)
                await bot.send_message(query.from_user.id, "Вы ответили верно. Вопрос {0}. {1} ".format(data['step'], data['quest']), reply_markup=markup)
        else:
            await bot.send_message(query.from_user.id, "Вы проиграли. Вы ответили неверно. Ответом было число {0}".format(correct))


@bot.message_handler(state=MyStates.number)
async def handler_number(message: Message):
    correct_num = 13
    chat_id = message.chat.id
    request = message.text
    if await validate_number(request):
        await get_answer(request, chat_id, "number")
        mes = "Ваш ответ принят: {0}".format(request)
    else:
        mes = "Ответ написан с ошибкой. Напишите ответ без пробелов и сторонних символов. Сейчас он выглядит так: {0}".format(request)
    if await check_correct_number(correct_num, int(request)):
        mes = "{0} Вы посчитали правильно!".format(mes)
    else:
        mes = "{0} К сожалению, вы ошиблись. Правильный ответ был {1}. У гусеницы {1} ножек.".format(mes,correct_num)
    await bot.set_state(message.from_user.id, MyStates.bird, chat_id)
    await bot.send_message(chat_id, mes)
    markup = await add_answer_kb(105,6,28)
    await bot.send_message(chat_id, "Вопрос 2. Сколько птиц пролетело за окном. Введите ваш ответ: ",
                           reply_markup=markup)
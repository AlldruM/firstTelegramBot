import telebot
from telebot import types
import datetime
import time
from threading import Thread
import cfg

bot = telebot.TeleBot(cfg.TOKEN)

users = []
user = cfg.CHAT_TEST_ID
const = 365
dembel = 103


@bot.message_handler(commands=['start','description','help']) # обработка кнопки /start в боте
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton("Описание")
    btn3 = types.KeyboardButton("Помощь")
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, 'Функция в разработке, но скоро станет доступна',  reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callbackMessage(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'answer':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Удалить сообщение", callback_data="delete")
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton("Отлично", callback_data="good")
        btn3 = types.InlineKeyboardButton("Устал, хочу кушать и спать", callback_data="tired")
        markup.row(btn2, btn3)
        bot.edit_message_text('Неплохо, как у Вас дела?', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'good':
            markUp = types.InlineKeyboardMarkup()
            btn1_1 = types.InlineKeyboardButton("Удалить сообщение", callback_data="delete")
            markUp.row(btn1_1)
            bot.edit_message_text('Я очень рад. Так держать', callback.message.chat.id, callback.message.message_id, reply_markup=markUp)
    elif callback.data == 'tired':
            markUp = types.InlineKeyboardMarkup()
            btn1_1 = types.InlineKeyboardButton("Удалить сообщение", callback_data="delete")
            markUp.row(btn1_1)
            bot.edit_message_text('Предлагаю все бросить и отдохнуть. Берегите себя!', callback.message.chat.id, callback.message.message_id, reply_markup=markUp)
    elif callback.data == 'edit':
            bot.edit_message_text('Функция в разработке, но скоро станет доступна <span class="tg-spoiler">(ОтсылОЧКА на Яндекс)</span>', callback.message.chat.id, callback.message.message_id, parse_mode='HTML')


@bot.message_handler(commands=['start', 'help'])
def start(message):
    user = message.chat.id
    bot.send_message(user, "https://www.youtube.com/watch?v=rdg4lkgsQ04")

@bot.message_handler(commands=['spam'])
def add_user(message):
    global user
    global const,dembel
    user = message.chat.id
    offset = datetime.timedelta(hours=3)
    immediately = datetime.datetime.now(tz=datetime.timezone(offset, 'MSK'))
    cuurent_date = immediately.strftime("%d.%m.%Y %H:%M:%S")
    if user not in users:
        users.append(user)
    #bot.send_message(user, f'#игорьдембель{const - dembel}')
    bot.send_message(user, f'С сегодняшнего дня, а именно {cuurent_date}, я буду считать дни до дембеля Игоря🫡. Надеюсь, я буду это делать исправно!')
    bot.send_message(user, f'#игорьдембель{const - dembel}')

@bot.message_handler(commands=['stop'])
def remove_user(message):
    user = message.chat.id
    users.remove(user)
    bot.send_message(user, "Все, все.")

def spam():
    global users
    offset = datetime.timedelta(hours=3)
    global const, dembel
    while True:
        immediately = datetime.datetime.now(tz=datetime.timezone(offset, 'MSK'))
        current_time = immediately.strftime("%H:%M")
        for user in users:
            if dembel == const:
                bot.send_message(user, 'Всё, всех поздравляю! Год прошёл, юху-у-у!')
                file = open('./Vse_GIF.mp4', 'rb')
                bot.send_animation(user, file)
                users.remove(user)
            elif current_time == '18:55':
                bot.send_message(user, f'#игорьдембель{const - dembel}')
                time.sleep(24*3600) # время, через которое отправляется команда выше
                dembel=dembel+1

@bot.message_handler(content_types='text')
def info(message):
    if message.text.lower() =='привет' or message.text.lower() =='ку':
        markUp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Удалить сообщение", callback_data='delete')
        markUp.row(btn1)
        btn2 = types.InlineKeyboardButton("Как дела?", callback_data='answer')
        btn3 = types.InlineKeyboardButton("Чем занимаешься?", callback_data="edit")
        markUp.row(btn2, btn3)
        bot.send_message(message.chat.id, f'Ты добр, {message.from_user.first_name} {message.from_user.last_name}',
                         reply_markup=markUp)
    elif message.text.lower() =='описание':
        bot.send_message(message.chat.id, 'Этот бот создан для автоматического подсчёта дней до дембеля Игоря🫡')
    elif message.text.lower() =='помощь':
        bot.send_message(message.chat.id, 'По всем вопросом, насчёт бота, обращаться: https://t.me/AlldruM')
    elif message.text.lower() != 'привет' or message.text.lower() != 'ку':
        file = open('./AnimatedSticker.tgs', 'rb')
        bot.send_sticker(message.chat.id, file)


spam_thread = Thread(target=spam)

spam_thread.start()
bot.polling(none_stop=True) # опрос методом polling(с англ. - опрос) с параметром none_stop - происходит бесконечно

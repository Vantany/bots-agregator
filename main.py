import os
from dotenv import load_dotenv
import telebot
import logging as log
from data import db_session
from data.bots import Bot

log.basicConfig(
    level=log.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        log.FileHandler('bot.log'),
        log.StreamHandler()
    ]
)

load_dotenv()

BOT_KEY = os.getenv("BOT_KEY")
bot = telebot.TeleBot(BOT_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    log.info(f'Команда /start от пользователя: {message.from_user.id}')

    chat_id = message.chat.id

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="Добавить бота",
                                              callback_data = "add_bot"),\
                telebot.types.InlineKeyboardButton(text="Список ботов",
                                             callback_data = "bot_list"))

    bot.send_message(chat_id, "Добро пожаловать!", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "add_bot")
def add_bot(call):
    log.info(f'Команда /add_bot от пользователя: {call.from_user.id}')

    pass


@bot.callback_query_handler(func=lambda call: call.data == "bot_list")
def bot_list(call):
    log.info(f'Команда /bot_list от пользователя: {call.from_user.id}')

    db_sess = db_session.create_session()
    bots = db_sess.query(Bot).all()
    db_sess.close()

    message_text = "Список ботов:\n"
    for ind, element in enumerate(bots[:5]):
        message_text += f"{ind + 1}.\n"
        message_text += f"Название: {element.name}\n"
        message_text += f"Ссылка: {element.url}\n"
        message_text += f"Описание: {element.description}\n\n"

    bot.send_message(call.message.chat.id, message_text)    


if __name__ == '__main__':
    db_session.global_init("db/data.db")

    log.info("Бот успешно запущен")
    bot.polling()
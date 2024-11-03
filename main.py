import os
from dotenv import load_dotenv
import telebot
import logging as log
from data import db_session

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


@bot.message_handler(commands=['start'])
def send_welcome(message):
    log.info(f'Команда /start от пользователя: {message.from_user.id}')
    bot.reply_to(message, "Добро пожаловать!")


if __name__ == '__main__':
    db_session.global_init("db/data.db")

    log.info("Бот успешно запущен")
    bot.polling()
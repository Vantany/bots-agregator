import os
import json
from dotenv import load_dotenv
import telebot
import logging as log
from data import db_session
from data.bots import Bot
from handlers import message_handlers,\
                         callback_handlers


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


#Подключаем обработчики событий
callback_handlers(bot)
message_handlers(bot)


if __name__ == '__main__':
    db_session.global_init("db/data.db")

    log.info("Бот успешно запущен")
    bot.polling()
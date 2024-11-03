import os
import json
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
    web_app_url = telebot.types.WebAppInfo("https://d185-94-231-132-242.ngrok-free.app")
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.add(telebot.types.KeyboardButton(text="Добавить бота",
                                              web_app = web_app_url),\
                telebot.types.KeyboardButton(text="Список ботов"))

    bot.send_message(chat_id, "Добро пожаловать!", reply_markup=keyboard)
    

@bot.message_handler(content_types="web_app_data")
def add_bot(webAppMes):
    data = json.loads(webAppMes.web_app_data.data)

    db_sess = db_session.create_session()
    new_bot = Bot(data["name"], data["url"], data["description"])
    db_sess.add(new_bot)
    db_sess.commit()
    db_sess.close()

    bot.send_message(webAppMes.chat.id, f"Бот успешно добавлен:\
                      \nНазвание: {data['name']}\
                      \nСсылка: {data['url']}\
                      \nОписание: {data['description']}")


@bot.message_handler(func=lambda message: message.text == "Список ботов")
def bot_list(message):
    log.info(f'Команда /bot_list от пользователя: {message.from_user.id}')

    db_sess = db_session.create_session()
    bots = db_sess.query(Bot).all()
    db_sess.close()

    message_text = ""
    for ind, element in enumerate(bots[:5]):
        message_text += f"{ind + 1}.\n"
        message_text += f"Название: {element.name}\n"
        message_text += f"Ссылка: {element.url}\n"
        message_text += f"Описание: {element.description}\n\n"

    bot.send_message(message.chat.id, message_text)    


if __name__ == '__main__':
    db_session.global_init("db/data.db")

    log.info("Бот успешно запущен")
    bot.polling()
import telebot
import json
import os
from dotenv import load_dotenv
import logging as log
from data import db_session
from data.bots import Bot
from functions import get_switching_keyboard

load_dotenv()

def message_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        """
        Хэндлер для обработки команды \start и \help,
        выводит на экран клавиатуру с действиями"""

        log.info(f'Команда /start от пользователя: {message.from_user.id}')

        chat_id = message.chat.id
        web_app_url = telebot.types.WebAppInfo("https://7c65-94-231-132-242.ngrok-free.app/form/")
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(telebot.types.KeyboardButton(text="Добавить бота",
                                                web_app = web_app_url),\
                    telebot.types.KeyboardButton(text="Список ботов"))

        bot.send_message(chat_id, "Добро пожаловать!", reply_markup=keyboard)\


    @bot.message_handler(func=lambda message: message.text == "Список ботов")
    def bot_list(message):
        """
        Хэндлер для обработки команды /bot_list,
        выводит на экран список ботов"""

        log.info(f'Команда /bot_list от пользователя: {message.from_user.id}')

        db_sess = db_session.create_session()
        current_bot = db_sess.query(Bot).where(Bot.id == 1).first()
        db_sess.close()

        if not current_bot:
            bot.send_message(message.chat.id, "Список ботов пуст")
            return

        message_text = f"*Название:* {current_bot.name}\n" + \
                        f"*Ссылка:* {current_bot.url}\n" + \
                        f"*Описание:* {current_bot.description}"

        
        bot.send_photo(message.chat.id, current_bot.image, caption=message_text,\
                        reply_markup=get_switching_keyboard(1),
                        parse_mode="Markdown")
        

    @bot.message_handler(content_types="web_app_data")
    def add_bot(webAppMes):
        """
        Хэндлер открывающий получающий json из
        webapp с формой, создает запись в таблице bots
        с новым ботом"""

        data = json.loads(webAppMes.web_app_data.data)

        try:
            print(webAppMes.web_app_data)
            db_sess = db_session.create_session()
            new_bot = Bot(data["name"], data["url"], data["description"], data["image"])
            db_sess.add(new_bot)
            db_sess.commit()
            db_sess.close()

            log.info(f"Бот успешно добавлен: {data['name']}")
        except Exception as e:
            log.info(f"Ошибка при добавлении бота: {e}")

        bot.send_photo(webAppMes.chat.id, data["image"], caption=f"Бот успешно добавлен:\
                        \nНазвание: {data['name']}\
                        \nСсылка: {data['url']}\
                        \nОписание: {data['description']}")

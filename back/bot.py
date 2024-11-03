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


def get_bots_amount() -> int:
    """
    Функция для подсчета колличества ботов в БД
    :return: кол-во ботов"""
    db_sess = db_session.create_session()
    amount = db_sess.query(Bot).count()
    db_sess.close()
    return amount


def get_switching_keyboard(page_num: int) -> telebot.types.InlineKeyboardMarkup:
    """
    Функция для создания клавиатуры, переключающей вкладки
    с карточками ботов
    :param page_num: номер страницы - id из таблицы bots
    :return: клавиатура типа InlineKeyboardMarkup"""
    bots_amount = get_bots_amount()

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="<<", callback_data=f"page_{page_num-1 if page_num > 1 else bots_amount}"),
                 telebot.types.InlineKeyboardButton(text=f"{page_num}/{bots_amount}", callback_data=f"{page_num}"),
                 telebot.types.InlineKeyboardButton(text=">>", callback_data=f"page_{page_num+1 if page_num < bots_amount else 1}"))
    return keyboard


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Хэндлер для обработки команды \start и \help,
    выводит на экран клавиатуру с действиями"""

    log.info(f'Команда /start от пользователя: {message.from_user.id}')

    chat_id = message.chat.id
    web_app_url = telebot.types.WebAppInfo("https://d185-94-231-132-242.ngrok-free.app")
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(telebot.types.KeyboardButton(text="Добавить бота",
                                              web_app = web_app_url),\
                telebot.types.KeyboardButton(text="Список ботов"))

    bot.send_message(chat_id, "Добро пожаловать!", reply_markup=keyboard)
    

@bot.message_handler(content_types="web_app_data")
def add_bot(webAppMes):
    """
    Хэндлер открывающий получающий json из
    webapp с формой, создает запись в таблице bots
    с новым ботом"""

    data = json.loads(webAppMes.web_app_data.data)

    try:
        db_sess = db_session.create_session()
        new_bot = Bot(data["name"], data["url"], data["description"])
        db_sess.add(new_bot)
        db_sess.commit()
        db_sess.close()

        log.info(f"Бот успешно добавлен: {data['name']}")
    except Exception as e:
        log.info(f"Ошибка при добавлении бота: {e}")

    bot.send_message(webAppMes.chat.id, f"Бот успешно добавлен:\
                      \nНазвание: {data['name']}\
                      \nСсылка: {data['url']}\
                      \nОписание: {data['description']}")


@bot.message_handler(func=lambda message: message.text == "Список ботов")
def bot_list(message):
    """
    Хэндлер для обработки команды /bot_list,
    выводит на экран список ботов"""

    log.info(f'Команда /bot_list от пользователя: {message.from_user.id}')

    db_sess = db_session.create_session()
    current_bot = db_sess.query(Bot).where(Bot.id == 1).first()
    db_sess.close()

    message_text = f"*Название:* {current_bot.name}\n" + \
                    f"*Ссылка:* {current_bot.url}\n" + \
                    f"*Описание:* {current_bot.description}"

    
    bot.send_message(message.chat.id, message_text,\
                     reply_markup=get_switching_keyboard(1),
                     parse_mode="Markdown")    


@bot.callback_query_handler(func=lambda call: call.data.startswith("page_"))
def switch_page(call):
    """
    Хэндлер для обработки нажатия на кнопки переключения страниц
    с карточками ботов"""

    page_num = int(call.data.split("_")[1])

    db_sess = db_session.create_session()
    current_bot = db_sess.query(Bot).where(Bot.id == page_num).first()
    db_sess.close()

    message_text = f"Название: {current_bot.name}\n" + \
                    f"Ссылка: {current_bot.url}\n" + \
                    f"Описание: {current_bot.description}"

    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, message_text,\
                        reply_markup=get_switching_keyboard(page_num))
        
        log.info(f"Пользователь {call.from_user.id} перешел на страницу {page_num}")
    except Exception as e:
        log.info(f"При переходе пользователя {call.from_user.id} страницу {page_num} произошла ошибка {e}")


if __name__ == '__main__':
    db_session.global_init("db/data.db")

    log.info("Бот успешно запущен")
    bot.polling()
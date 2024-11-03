import os
from dotenv import load_dotenv
import telebot

load_dotenv()

BOT_KEY = os.getenv("BOT_KEY")
bot = telebot.TeleBot(BOT_KEY)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
                Just Check work condition""")
    

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
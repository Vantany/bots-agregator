import telebot
from functions import get_bots_amount

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
import telebot
import logging as log
from data import db_session
from data import Bot
from functions import get_switching_keyboard

def callback_handlers(bot: telebot.TeleBot):
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
            bot.send_photo(call.message.chat.id, current_bot.image, caption=message_text,\
                        reply_markup=get_switching_keyboard(page_num),
                        parse_mode="Markdown")    

            
            log.info(f"Пользователь {call.from_user.id} перешел на страницу {page_num}")
        except Exception as e:
            log.info(f"При переходе пользователя {call.from_user.id} страницу {page_num} произошла ошибка {e}")
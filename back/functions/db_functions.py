from data import db_session
from data.bots import Bot

def get_bots_amount() -> int:
    """
    Функция для подсчета колличества ботов в БД
    :return: кол-во ботов"""
    db_sess = db_session.create_session()
    amount = db_sess.query(Bot).count()
    db_sess.close()
    return amount
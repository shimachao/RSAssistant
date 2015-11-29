#-*-coding:UTF-8-*-

from websession import WebSession, TimeoutError, RepeatSignError
from db import DB
from time import sleep
import arrow


def sign():
    """ 签到
    """
    try:
        rs_web = WebSession(username='高手情结', password='531236305')
        rs_web.login()
        rs_web.turn_to_sign_page()
        rs_web.sign()
    except TimeoutError:
        rs_web.close()
        raise
    except RepeatSignError:
        rs_web.close()
        raise
    else:
        gold_num = rs_web.get_gold_num()
        return gold_num


def have_signed_already():
    db = DB(database='sign_records.db')
    r = db.select_today_record()
    db.close()

    return r is not None


def sleep_until_tomorrow_sign_time():
    now = arrow.now()
    tomorrow_sign_time = now.replace(days=1, hour=7, minute=1, second=0)
    seconds = (tomorrow_sign_time - now).total_seconds()
    sleep(seconds)


def is_sign_time_now():
    """ 判断当前时间是不是签到时间"""
    now = arrow.now()
    dt_start = now.replace(hour=7, minute=0, second=0)
    dt_end = now.replace(hour=23, minute=59, second=0)

    return dt_start < now < dt_end


def sleep_until_today_sign_time():
    now = arrow.now()
    sign_start_time = now.replace(hour=7, minute=0, second=0)
    seconds = (sign_start_time - now).total_seconds()
    sleep(seconds)


def sign_service():
    while True:
        if have_signed_already():
            sleep_until_tomorrow_sign_time()

        if not is_sign_time_now():
            sleep_until_today_sign_time()

        try:
            gold_num = sign()
        except TimeoutError:
            sleep(5*50)
        except RepeatSignError:
            sleep_until_tomorrow_sign_time()
        else:
            db = DB(database='sign_records.db')
            db.insert(gold=gold_num)
            db.close()
            sleep_until_tomorrow_sign_time()

if __name__ == '__main__':
    sign_service()

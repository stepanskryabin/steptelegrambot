#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CONFIG FILE

import os

# Pascal to mercury pole millimeters conversion constant
CONSTANT_PA_TO_MPM: float = 7.5006E-3

# Configuring database access
# SQLite3
LOCAL_SQLITE = ''.join(['sqlite:', os.path.abspath('bot_database.db')])
# PostgreSQL
LOCAL_POSTGRESQL = 'postgres://testdb:123456@127.0.0.1/test_telegrambot'
# PostgreSQL
ONLINE_POSTGRESQL = os.getenv('DATABASE_URL')

# Configuring OpenWeatherMap.org access
WEATHER_TOKEN_API = os.getenv('WEATHER_API')

# Configuring Telegram access
TELEGRAM_TOKEN_API = os.getenv('BOT_API')

# City list
CITY_LIST = os.path.abspath('city.list.json')

# Logging module settings
#
# Setting the debug message level

# Possible options:
# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG
MESSAGE_LEVEL = 'DEBUG'

# Log file storage location
#
FILENAME = './log/bot.log'

# File mode
# 'r' - open for reading (default)
# 'w' - open for writing, truncating the file first
# 'x' - open for exclusive creation, failing if the file already exists
# 'a' - open for writing, appending to the end of the file if it exists
# 'b' - binary mode
# 't' - text mode (default)
# '+' - open for updating (reading and writing)
# Possible options:
FILEMODE = 'w'

# Debug message output format
# %(asctime)s   -   Human-readable time when the LogRecord was created.
#                   By default this is of the form ‘2003-07-08 16:49:45,896’
#                   (the numbers after the comma are millisecond portion of the
#                   time).
# %(levelname)s -   Text logging level for the message ('DEBUG', 'INFO',
#                   'WARNING', 'ERROR', 'CRITICAL').
# %(funcName)s  -   Name of function containing the logging call.
# %(message)s   -   The logged message, computed as msg % args. This is set
#                   when Formatter.format() is invoked.
# Possible options:
FORMAT_MESSAGE = '%(asctime)s: %(levelname)s: %(funcName)s - %(message)s'

# Time format
# %Y - Year with century as a decimal number.
# %m - Month as a zero-padded decimal number.
# %d - Day of the month as a zero-padded decimal number.
# %H - Hour (24-hour clock) as a zero-padded decimal number.
# %M - Minute as a zero-padded decimal number.
# %S - Second as a zero-padded decimal number.
# Possible options:
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Message
START_MESSAGE = "Привет, я <b>Погодный бот!</b>\
    \nНапиши мне имя города, а я поищу информацию о погоде в нём.\
    \nЕсли нужна более подробная информация жми /help"

HELP_MESSAGE = "Этот бот помогает узнать погоду в твоём городе.\
    \nВведи название города, например: <b>Москва</b>\
    \nЕсли хочешь получать постоянные прогнозы, или персонифицировать\
    \nпрогноз, необходимо зарегистрироваться.\
    \nДля подробной информации о регистарции жми /register\
    \n\
    \nВерсия бота: {}"

REGISTER_MESSAGE = "\n Для регистрации аккаунта нажмите:\
    \n/reguser - после регистрации бот сохранит следующие данные:\
    \n\
    \nДля удаления аккаунта нажмите:\
    \n/deluser - ВНИМАНИЕ: будут удалены все настройки и личные данные! "

REGISTER_PROCEED = "Введите имя города"

"""
FORMAT MESSAGE:
    {1} - city_name
    {2} - description
    {3} - insert_emoji
    {4} - temp
    {5} - feels
    {6} - pressure
    {7} - humidity
    {8} - clouds
    {9} - speed_wing
"""
CURRENT_WEATHER_MESSAGE = "Сейчас в {} <b><i>{}</i></b> {}\
    \nТемпература: <b>{} C.</b>\
    \nЧувствуется как: <b>{} C.</b>\
    \nДавление: <b>{} мм.рт.ст.</b>\
    \nВлажность: <b>{} %.</b>\
    \nОблачность: <b>{} %.</b>\
    \nСкорость ветра: <b> {} метров в сек. </b>"

FORECAST_WEATHER_MESSAGE = "Сейчас в {} <b><i>{}</i></b> {}\
    \nТемпература: <b>{} C.</b>\
    \nЧувствуется как: <b>{} C.</b>\
    \nДавление: <b>{} мм.рт.ст.</b>\
    \nВлажность: <b>{} %.</b>\
    \nОблачность: <b>{} %.</b>\
    \nСкорость ветра: <b> {} метров в сек. </b>"

ONECALL_WEATHER_MESSAGE = "Сейчас в {} <b><i>{}</i></b> {}\
    \nТемпература: <b>{} C.</b>\
    \nЧувствуется как: <b>{} C.</b>\
    \nДавление: <b>{} мм.рт.ст.</b>\
    \nВлажность: <b>{} %.</b>\
    \nОблачность: <b>{} %.</b>\
    \nСкорость ветра: <b> {} метров в сек. </b>"


EMOJI_DICT = {
    200: '\U00002744',
    201: '\U000026A1',
    202: '\U000026A1',
    210: '\U000026C5',
    211: '\U000026C5',
    212: '\U000026C5',
    221: '\U000026C5',
    230: '\U000026A1',
    231: '\U000026A1',
    232: '\U000026A1',
    300: '\U00002614',
    301: '\U00002614',
    302: '\U00002614',
    310: '\U00002614',
    311: '\U00002614',
    312: '\U00002614',
    313: '\U00002614',
    314: '\U00002614',
    321: '\U00002614',
    500: '\U0001F302',
    501: '\U0001F302',
    502: '\U0001F302',
    503: '\U0001F302',
    504: '\U0001F302',
    511: '\U00002614',
    520: '\U00002614',
    521: '\U00002614',
    522: '\U00002614',
    531: '\U00002614',
    600: '\U00002744',
    601: '\U00002744',
    602: '\U00002744',
    611: '\U00002744',
    612: '\U00002744',
    613: '\U00002744',
    614: '\U00002744',
    615: '\U00002744',
    616: '\U00002744',
    620: '\U00002744',
    621: '\U00002744',
    622: '\U00002744',
    701: '\U0001F301',
    711: '\U0001F301',
    712: '\U0001F301',
    721: '\U0001F301',
    731: '\U0001F301',
    741: '\U0001F301',
    751: '\U0001F301',
    761: '\U0001F301',
    762: '\U0001F301',
    771: '\U0001F301',
    781: '\U0001F300',
    800: '\U000026C5',
    801: '\U00002601',
    802: '\U00002601',
    803: '\U000026C5',
    804: '\U00002601'
}

USER_ALREDY_REGISTERED = "Пользователь: {} с ID {} уже зарегистрирован."

USER_IS_REGISTERED = "Пользователь: {} с ID: {} создан."

USER_IS_DELETED = "Пользователь: {} с ID: {} удалён."

USER_NOT_EXIST = "Пользователя: {} с ID: {} не существует."

INFO_NOT_FOUND = "Информация не найдена"

FUNCTION_FOR_REGISTERED_USER = "Функция доступна только зарегистрированному \
    пользователю"

USER_INFO = "Персональные настройки:\
    ID: {}\
    Город: {}, долгота - {}, широта - {}\
    Настройки оповещения:\
        периодичность (часы) - {}\
        периодичность (дни) - {}\
        периодичность (количество раз) - {}"

if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

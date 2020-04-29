#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CONFIG FILE

import os

# Stiker Welcome
W_STICKER: str = './welcome.webp'

# Sticker
STICKER_ID: str = 'CAACAgIAAxkBAANhXkkWbDoQR15v86aV-lx0S5nrjfkAAqQAAwLV8A8r2CzEaz_SZBgE'

# Pascal to mercury pole millimeters conversion constant
CONSTANT_PA_TO_MPM: float = 7.5006E-3

# Configuring database access
# SQLite3
LOCAL_SQLITE = 'sqlite:' + os.path.abspath('bot_database.db')
# PostgreSQL
LOCAL_POSTGRESQL = 'postgres://testdb:123456@127.0.0.1/test_telegrambot'
# PostgreSQL
ONLINE_POSTGRESQL = os.getenv('DATABASE_URL')


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
# %(asctime)s -    Human-readable time when the LogRecord was created.
#                  By default this is of the form ‘2003-07-08 16:49:45,896’
#                  (the numbers after the comma are millisecond portion of the time).
# %(levelname)s -  Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
# %(funcName)s -   Name of function containing the logging call.
# %(message)s -    The logged message, computed as msg % args. This is set when Formatter.format() is invoked.
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
    \n/deluser - ВНИМАНИЕ: будут удалены все настройки и личные данные!"


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

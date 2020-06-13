#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NAME = ПогодныйБот
# BOT NICKNAME = StepTelegramBot
# Autor: Stepan Skriabin
# email: stepan.skrjabin@gmail.com
__version__ = '0.0.10b1'

from telebot import TeleBot
from telebot.types import Message
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ReplyKeyboardRemove
from telebot.types import KeyboardButton
import sqlobject as orm

import app.config as config
from app.controller import check_user_in_db
from app.controller import write_user_in_db
from app.controller import delete_user_in_db
from app.controller import read_user_in_db
from app.controller import hash_password
from app.controller import UserConfig

from plug.weather import search_weather, replace_name


bot = TeleBot(config.TELEGRAM_TOKEN_API)

"""
    Choose the option to connect to the userbase, where:
    LOCAL_SQLITE: bot_userbase.db file will be created
    in the local directory
    LOCAL_POSTGRESQL: connection to a local server
    ONLINE_POSTGRESQL: connection will be made to a server hosted
    on the Internet.

    The settings are in the file botconfig.py
"""
connection = orm.connectionForURI(config.LOCAL_SQLITE)
orm.sqlhub.processConnection = connection


# Return information about StepTelegramBot
@bot.message_handler(commands=['start'])
@bot.edited_message_handler(commands=['start'])
def handler_command_start(message: Message):
    bot.send_message(message.chat.id, config.START_MESSAGE,
                     parse_mode='HTML')
    return


# Return help information
@bot.message_handler(commands=['help'])
@bot.edited_message_handler(commands=['help'])
def handler_command_help(message: Message):
    bot.send_message(message.chat.id,
                     config.HELP_MESSAGE.format(__version__),
                     parse_mode='HTML')
    return


# Reply markup Keyboard
@bot.message_handler(commands=['menu'])
def markupConfig(message: Message):
    # "Back to menu" button
    backbtn = KeyboardButton('Назад в главное меню')
    # Main menu
    main_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    mainbtn1 = KeyboardButton('Погода')
    mainbtn2 = KeyboardButton('Настройки')
    mainbtn3 = KeyboardButton('Убрать меню')
    mainbtn4 = KeyboardButton('Тест')
    main_menu.add(mainbtn1, mainbtn2, mainbtn3, mainbtn4)
    # Weather menu
    weather_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    weatherbtn1 = KeyboardButton('Киров')
    weatherbtn2 = KeyboardButton('Кирово-Чепецк')
    weatherbtn3 = KeyboardButton('Ввести город')
    weather_menu.add(weatherbtn1, weatherbtn2, weatherbtn3, backbtn)
    # Configuration menu
    config_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    configbtn1 = KeyboardButton('Регистрация')
    configbtn2 = KeyboardButton('Удаление')
    configbtn3 = KeyboardButton('Показать настройки')
    configbtn4 = KeyboardButton('Месторасположение')
    configbtn5 = KeyboardButton('Уведомление')
    config_menu.add(configbtn1, configbtn2, configbtn3, configbtn4, configbtn5,
                    backbtn)
    # City config menu
    сity_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    сitybtn1 = KeyboardButton('Указать место')
    сitybtn2 = KeyboardButton('Определить место')
    сity_menu.add(сitybtn1, сitybtn2, backbtn)
    # Notice
    notice_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    noticebtn1 = KeyboardButton('Каждый час')
    noticebtn2 = KeyboardButton('Утром и вечером')
    noticebtn3 = KeyboardButton('Отключить')
    notice_menu.add(noticebtn1, noticebtn2, noticebtn3, backbtn)
    # Input menu
    input_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    input_menu.add(backbtn)
    # Test
    test_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    testbtn1 = KeyboardButton('Тест1')
    testbtn2 = KeyboardButton('Тест2')
    testbtn3 = KeyboardButton('Тест3')
    testbtn4 = KeyboardButton('Тест4')
    test_menu.add(testbtn1, testbtn2, testbtn3, testbtn4)

    def back_to_main_menu(message):
        msg = bot.reply_to(message, 'Возвращаемся в главное меню',
                           reply_markup=main_menu)
        bot.register_next_step_handler(msg, mainMenu)
        return

    def remove_menu(message):
        del_markup = ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, 'Для возврата в меню: /menu',
                         reply_markup=del_markup)

    def inputMenu(message: Message):
        if message.text == 'Назад в главное меню':
            back_to_main_menu(message)
            return
        else:
            result = search_weather(message.text, option='current')
            if result['cod'] == 200:
                bot.send_message(message.chat.id,
                                 config.CURRENT_WEATHER_MESSAGE.format(
                                  replace_name(result['name']),
                                  result['weather'][0]['description'],
                                  config.EMOJI_DICT[result['weather'][0]['id']],
                                  result['main']['temp'],
                                  result['main']['feels_like'],
                                  result['main']['pressure'],
                                  result['main']['humidity'],
                                  result['clouds']['all'],
                                  result['wind']['speed']),
                                 parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, config.INFO_NOT_FOUND)
            msg = bot.reply_to(message,
                               'Попробуйте снова',
                               reply_markup=input_menu)
            bot.register_next_step_handler(msg, inputMenu)
            return

    def noticeMenu(message: Message):
        if message.text == 'Каждый час':
            msg = bot.reply_to(message, 'НЕРАБОТАЕТ')
            bot.register_next_step_handler(msg, markupConfig)
        elif message.text == 'Утром и вечером':
            msg = bot.reply_to(message, 'НЕРАБОТАЕТ')
            bot.register_next_step_handler(msg, markupConfig)
        elif message.text == 'Отключить':
            msg = bot.reply_to(message, 'НЕРАБОТАЕТ')
            bot.register_next_step_handler(msg, markupConfig)
        elif message.text == 'Назад в главное меню':
            back_to_main_menu(message)
        else:
            return

    def сityMenu(message: Message):
        if message.text == 'Указать место':
            msg = bot.reply_to(message, 'НЕРАБОТАЕТ')
            bot.register_next_step_handler(msg, markupConfig)
        elif message.text == 'Определить место':
            msg = bot.reply_to(message, 'НЕРАБОТАЕТ')
            bot.register_next_step_handler(msg, markupConfig)
        elif message.text == 'Назад в главное меню':
            back_to_main_menu(message)
        else:
            return

    def configMenu(message: Message):
        user_id = message.from_user.id
        username = message.from_user.username
        if message.text == 'Регистрация':
            if check_user_in_db(user_id):
                bot.send_message(user_id,
                                 config.USER_ALREDY_REGISTERED.format(
                                  username,
                                  user_id)
                                 )
            else:
                user = UserConfig(message.from_user.id)
                user.first_name = message.from_user.first_name
                user.last_name = message.from_user.last_name
                user.username = message.from_user.username
                user.language_code = message.from_user.language_code
                user.is_bot = message.from_user.is_bot

                def step_town(message):
                    town: str = message.text
                    if town.isdigit():
                        msg = bot.reply_to(message, 'Это не незвание города, попробуйте повторно')
                        bot.register_next_step_handler(msg, step_town)
                    user.town = message.text
                    msg = bot.reply_to(message, 'Шаг 2: введите пароль')
                    bot.register_next_step_handler(msg, step_password)

                def step_password(message):
                    if len(message.text) < 6:
                        msg = bot.reply_to(message, 'Длинна пароля должна быть от 7 и более символов')
                        bot.register_next_step_handler(msg, step_password)
                    password = hash_password(message.text)
                    user.password = password['hash']
                    user.salt = password['salt']
                    msg = bot.reply_to(message, 'Шаг 3: введите периодичность вывода прогноза погоды, количестве раз в день')
                    bot.register_next_step_handler(msg, step_time)

                def step_time(message):
                    time: str = message.text
                    if not time.isdigit():
                        msg = bot.reply_to(message, 'Неверные данные, повторите ввод')
                        bot.register_next_step_handler(msg, step_time)
                    user.time = int(message.text)
                    msg = bot.reply_to(message, 'Шаг 4: введите количество дней на которые нужен прогноз')
                    bot.register_next_step_handler(msg, step_day)

                def step_day(message):
                    day: str = message.text
                    if not day.isdigit():
                        msg = bot.reply_to(message, 'Неверные данные, повторите ввод')
                        bot.register_next_step_handler(msg, step_day)
                    user.day = int(message.text)
                    msg = bot.reply_to(message, 'Шаг 5: введите quantity')
                    bot.register_next_step_handler(msg, step_quantity)

                def step_quantity(message):
                    quantity: str = message.text
                    if not quantity.isdigit():
                        msg = bot.reply_to(message, 'Неверные данные, повторите ввод')
                        bot.register_next_step_handler(msg, step_quantity)
                    user.quantity = int(message.text)
                    write_user_in_db(user.all_data())
                    bot.send_message(user_id,
                                     config.USER_IS_REGISTERED.format(
                                      message.from_user.username,
                                      message.from_user.id)
                                     )
                    msg = bot.reply_to(message, 'ЗАГЛУШКА1111', reply_markup=config_menu)
                    bot.register_next_step_handler(msg, configMenu)

                msg = bot.reply_to(message, 'Шаг 1: укажите город')
                bot.register_next_step_handler(msg, step_town)

        elif message.text == 'Удаление':
            if check_user_in_db(user_id):
                delete_user_in_db(user_id)
                bot.send_message(message.chat.id,
                                 config.USER_IS_DELETED.format(
                                  username,
                                  user_id)
                                 )
            else:
                bot.send_message(message.chat.id,
                                 config.USER_NOT_EXIST.format(
                                  username,
                                  user_id)
                                 )
            msg = bot.reply_to(message, 'ЗАГЛУШКА2222222', reply_markup=config_menu)
            bot.register_next_step_handler(msg, configMenu)
        elif message.text == 'Показать настройки':
            def check_password(message):
                passw = message.text
                print(passw)
                settings: dict = read_user_in_db(user_id)
                old_password = settings['password']
                old_salt = settings['salt']
                print(old_password, old_salt)
                new_password = hash_password(message.text, settings['salt'])
                if new_password['hash'] == settings['password']:
                    bot.send_message(user_id, config.USER_SETTINGS_INFO.format(
                                  settings['id'],
                                  settings['first_name'],
                                  settings['last_name'],
                                  settings['username'],
                                  settings['language_code'],
                                  settings['town'],
                                  settings['password'],
                                  settings['time'],
                                  settings['day'],
                                  settings['quantity']), parse_mode='HTML')
                else:
                    bot.send_message(message.chat.id,
                                     config.USER_NOT_EXIST.format(
                                      username,
                                      user_id)
                                     )
                msg = bot.reply_to(message, 'ЗАГЛУШКА333333', reply_markup=config_menu)
                bot.register_next_step_handler(msg, configMenu)

            msg = bot.reply_to(message, 'Введите пароль')
            bot.register_next_step_handler(msg, check_password)

        elif message.text == 'Месторасположение':
            msg = bot.reply_to(message, 'ЗАГЛУШКА', reply_markup=сity_menu)
            bot.register_next_step_handler(msg, сityMenu)
        elif message.text == 'Уведомление':
            msg = bot.reply_to(message, 'ЗАГЛУШКА', reply_markup=notice_menu)
            bot.register_next_step_handler(msg, noticeMenu)
        elif message.text == 'Назад в главное меню':
            back_to_main_menu(message)
        else:
            return

    def weatherMenu(message: Message):
        if message.text == 'Назад в главное меню':
            back_to_main_menu(message)
        elif message.text == 'Киров':
            result = search_weather(message.text, option='current')
            if result['cod'] == 200:
                bot.send_message(message.chat.id,
                                 config.CURRENT_WEATHER_MESSAGE.format(
                                  replace_name(result['name']),
                                  result['weather'][0]['description'],
                                  config.EMOJI_DICT[result['weather'][0]['id']],
                                  result['main']['temp'],
                                  result['main']['feels_like'],
                                  result['main']['pressure'],
                                  result['main']['humidity'],
                                  result['clouds']['all'],
                                  result['wind']['speed']),
                                 parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, config.INFO_NOT_FOUND)
            msg = bot.reply_to(message,
                               'Выберите город из списка или введите свой',
                               reply_markup=weather_menu)
            bot.register_next_step_handler(msg, weatherMenu)
        elif message.text == 'Кирово-Чепецк':
            result = search_weather(message.text, option='current')
            if result['cod'] == 200:
                bot.send_message(message.chat.id,
                                 config.CURRENT_WEATHER_MESSAGE.format(
                                  replace_name(result['name']),
                                  result['weather'][0]['description'],
                                  config.EMOJI_DICT[result['weather'][0]['id']],
                                  result['main']['temp'],
                                  result['main']['feels_like'],
                                  result['main']['pressure'],
                                  result['main']['humidity'],
                                  result['clouds']['all'],
                                  result['wind']['speed']),
                                 parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, config.INFO_NOT_FOUND)
            msg = bot.reply_to(message,
                               'Выберите город из списка или введите свой',
                               reply_markup=weather_menu)
            bot.register_next_step_handler(msg, weatherMenu)
        elif message.text == 'Ввести город':
            msg = bot.reply_to(message, 'Введите город', reply_markup=input_menu)
            bot.register_next_step_handler(msg, inputMenu)
        else:
            return

    def testMenu(message: Message):
        if message.text == 'Тест1':
            param = message.chat.id, 'TEST1'
            bot.send_message(message.chat.id, 'TEST1')
            bot.register_for_reply(bot.send_message, *param)
        elif message.text == 'Тест2':
            param = message.chat.id, 'TEST2'
            bot.register_next_step_handler(message.text, bot.send_message, *param)
        elif message.text == 'Тест3':
            bot.clear_step_handler(message)
        elif message.text == 'Тест4':
            back_to_main_menu(message)

    def mainMenu(message: Message):
        if message.text == 'Погода':
            msg = bot.reply_to(message, 'Выберите город из списка или введите свой', reply_markup=weather_menu)
            bot.register_next_step_handler(msg, weatherMenu)
        elif message.text == 'Настройки':
            msg = bot.reply_to(message, 'Настройки', reply_markup=config_menu)
            bot.register_next_step_handler(msg, configMenu)
        elif message.text == 'Тест':
            msg = bot.reply_to(message, 'Меню для тестирования функций', reply_markup=test_menu)
            bot.register_next_step_handler(msg, testMenu)
        elif message.text == 'Убрать меню':
            remove_menu(message)
        else:
            return

    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    msg = bot.reply_to(message, "Выберете пункт меню", reply_markup=main_menu)
    bot.register_next_step_handler(msg, mainMenu)

"""
# Return current weather in fixed city for registred User
@bot.message_handler(commands=['current'])
@bot.edited_message_handler(commands=['current'])
def handler_command_current(message: Message):
    result = Users.select(Users.q.userTown == message.from_user.id)
    if bool(result.count()):
        town = result[0].userTown
        result = search_weather(town, option='current')
        write_current(result)
    else:
        bot.send_message(
            message.chat.id, config.FUNCTION_FOR_REGISTERED_USER)
        return
    result = CurrentWeather.selectBy(
        dateTime=result['dt'], cityName=town)
    if bool(result.count()):
        bot.send_message(message.chat.id,
                         config.CURRENT_WEATHER_MESSAGE.format(
                             replace_name(result[0].cityName),
                             result[0].weatherDescription,
                             config.EMOJI_DICT[result[0].weatherId],
                             result[0].mainTemp,
                             result[0].mainFeelsLike,
                             result[0].mainPressure,
                             result[0].mainHumidity,
                             result[0].cloudsAll,
                             result[0].windSpeed
                         ), parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, config.INFO_NOT_FOUND)
    return


# Return forecast weather in fixed city for registred User
@bot.message_handler(commands=['forecast'])
@bot.edited_message_handler(commands=['forecast'])
def handler_command_forecast(message: Message):
    result = Users.select(Users.q.userId == message.from_user.id)
    if bool(result.count()):
        town = result[0].userTown
        result = search_weather(town, option='forecast')
        write_forecast(result)
    else:
        bot.send_message(
            message.chat.id, config.FUNCTION_FOR_REGISTERED_USER)
        return
    result = ForecastWeather.selectBy(
        dateTime=result['dt'], cityName=town)
    if bool(result.count()):
        bot.send_message(message.chat.id,
                         config.FORECAST_WEATHER_MESSAGE.format(
                             replace_name(result[0].cityName),
                             result[0].weatherDescription,
                             config.EMOJI_DICT[result[0].weatherId],
                             result[0].mainTemp,
                             result[0].mainFeelsLike,
                             result[0].mainPressure,
                             result[0].mainHumidity,
                             result[0].cloudsAll,
                             result[0].windSpeed
                         ), parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, config.INFO_NOT_FOUND)
    return


# Return onecall weather in fixed city for registred User
@bot.message_handler(commands=['onecall'])
@bot.edited_message_handler(commands=['onecall'])
def handler_command_onecall(message: Message):
    result = Users.select(Users.q.userId == message.from_user.id)
    if bool(result.count()):
        lon = result[0].userTownLon
        lat = result[0].userTownLat
        town = result[0].userTown
        result = search_weather(town, option='onecall', lon=lon, lat=lat)
        write_onecall(result)
    else:
        bot.send_message(
            message.chat.id, config.FUNCTION_FOR_REGISTERED_USER)
        return
    result = OnecallWeather.selectBy(
        dateTime=result['dt'], lon=lon, lat=lat)
    if bool(result.count()):
        bot.send_message(message.chat.id,
                         config.ONECALL_WEATHER_MESSAGE.format(
                             replace_name(result[0].cityName),
                             result[0].weatherDescription,
                             config.EMOJI_DICT[result[0].weatherId],
                             result[0].mainTemp,
                             result[0].mainFeelsLike,
                             result[0].mainPressure,
                             result[0].mainHumidity,
                             result[0].cloudsAll,
                             result[0].windSpeed
                         ), parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, config.INFO_NOT_FOUND)
    return
"""


# RUN
print('StepTelegramBot is running')
bot.polling(timeout=900)

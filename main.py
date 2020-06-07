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
from app.controller import check_user, write_user, delete_user, read_user

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



    bot.send_message(message.chat.id,
                     config.REGISTER_MESSAGE,
                     parse_mode='HTML')
    return


# Reply markup Keyboard
@bot.message_handler(commands=['menu'])
def markupConfig(message: Message):
    # Main menu
    main_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    mainbtn1 = KeyboardButton('Погода')
    mainbtn2 = KeyboardButton('Настройки')
    mainbtn3 = KeyboardButton('Убрать меню')
    main_menu.add(mainbtn1, mainbtn2, mainbtn3)
    # Weather menu
    weather_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    weatherbtn1 = KeyboardButton('Киров')
    weatherbtn2 = KeyboardButton('Кирово-Чепецк')
    weatherbtn3 = KeyboardButton('Ввести город')
    weatherbtn4 = KeyboardButton('Назад в главное меню')
    weather_menu.add(weatherbtn1, weatherbtn2, weatherbtn3, weatherbtn4)
    # Configuration menu
    config_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    configbtn1 = KeyboardButton('Регистрация')
    configbtn2 = KeyboardButton('Удаление')
    configbtn3 = KeyboardButton('Показать настройки')
    configbtn4 = KeyboardButton('Месторасположение')
    configbtn5 = KeyboardButton('Уведомление')
    configbtn6 = KeyboardButton('Назад в главное меню')
    config_menu.add(configbtn1, configbtn2, configbtn3, configbtn4, configbtn5,
                    configbtn6)
    # City menu
    сity_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    сitybtn1 = KeyboardButton('Указать место')
    сitybtn2 = KeyboardButton('Определить место')
    сitybtn3 = KeyboardButton('Назад в главное меню')
    сity_menu.add(сitybtn1, сitybtn2, сitybtn3)
    # Notice
    notice_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    noticebtn1 = KeyboardButton('Каждый час')
    noticebtn2 = KeyboardButton('Утром и вечером')
    noticebtn3 = KeyboardButton('Отключить')
    noticebtn4 = KeyboardButton('Назад в главное меню')
    notice_menu.add(noticebtn1, noticebtn2, noticebtn3, noticebtn4)

    def noticeMenu(message: Message):
        text = message.text
        if text == 'Каждый час':
            msg = bot.reply_to(message, 'НЕРАБОТАЕТ')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Утром и вечером':
            msg = bot.reply_to(message, 'НЕРАБОТАЕТ')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Отключить':
            msg = bot.reply_to(message, 'НЕРАБОТАЕТ')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Назад в главное меню':
            msg = bot.reply_to(message, 'НЕРАБОТАЕТ', reply_markup=main_menu)
            bot.register_next_step_handler(msg, markupConfig)
        else:
            return

    def сityMenu(message: Message):
        text = message.text
        if text == 'Указать место':
            msg = bot.reply_to(message, 'НЕРАБОТАЕТ')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Определить место':
            msg = bot.reply_to(message, 'НЕРАБОТАЕТ')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Назад в главное меню':
            msg = bot.reply_to(message, 'НЕРАБОТАЕТ', reply_markup=main_menu)
            bot.register_next_step_handler(msg, markupConfig)
        else:
            return

    def configMenu(message: Message):
        text: str = message.text
        user: dict = {
                'id': message.from_user.id,
                'first_name': message.from_user.first_name,
                'last_name': message.from_user.last_name,
                'username': message.from_user.username,
                'language_code': message.from_user.language_code,
                'is_bot': message.from_user.is_bot,
                'town': None,
                'password': None,
                'time': None,
                'day': None,
                'quantity': None
                  }
        while True:
            if text == 'Регистрация':
                if check_user(user['id']):
                    bot.send_message(user['id'],
                                     config.USER_ALREDY_REGISTERED.format(
                                      user['username'],
                                      user['id'])
                                     )
                else:
                    write_user(user)
                    bot.send_message(user['id'],
                                     config.USER_IS_REGISTERED.format(
                                      user['username'],
                                      user['id'])
                                     )
                msg = bot.reply_to(message, 'ЗАГЛУШКА1111', reply_markup=config_menu)
                bot.register_next_step_handler(msg, configMenu)
                break
            elif text == 'Удаление':
                if check_user(user['id']):
                    delete_user(user['id'])
                    bot.send_message(message.chat.id,
                                     config.USER_IS_DELETED.format(
                                      user['username'],
                                      user['id'])
                                     )
                else:
                    bot.send_message(message.chat.id,
                                     config.USER_NOT_EXIST.format(
                                      user['username'],
                                      user['id'])
                                     )
                msg = bot.reply_to(message, 'ЗАГЛУШКА2222222', reply_markup=config_menu)
                bot.register_next_step_handler(msg, configMenu)
                break
            elif text == 'Показать настройки':
                if check_user(user['id']):
                    settings: dict = read_user(user['id'])
                    bot.send_message(user['id'], config.USER_SETTINGS_INFO.format(
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
                                      user['username'],
                                      user['id'])
                                     )
                msg = bot.reply_to(message, 'ЗАГЛУШКА333333', reply_markup=config_menu)
                bot.register_next_step_handler(msg, configMenu)
                break
            elif text == 'Месторасположение':
                msg = bot.reply_to(message, 'ЗАГЛУШКА', reply_markup=сity_menu)
                bot.register_next_step_handler(msg, сityMenu)
                break
            elif text == 'Уведомление':
                msg = bot.reply_to(message, 'ЗАГЛУШКА', reply_markup=notice_menu)
                bot.register_next_step_handler(msg, noticeMenu)
                break
            elif text == 'Назад в главное меню':
                msg = bot.reply_to(message, 'ЗАГЛУШКА', reply_markup=main_menu)
                bot.register_next_step_handler(msg, markupConfig)
                break
        else:
            return

    def weatherMenu(message: Message):
        text: str = message.text
        while True:
            if text == 'Назад в главное меню':
                bot.send_message(message, 'Возврат в главное меню', reply_markup=main_menu)
                bot.register_next_step_handler(message, markupConfig)
                break
            elif text == 'Киров':
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
                bot.send_message(message,
                                 f'Команда {message.text} не распознана',
                                 reply_markup=weather_menu)
                bot.register_next_step_handler(message, weatherMenu)
                break
            elif text == 'Кирово-Чепецк':
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
                bot.send_message(message,
                                 f'Команда {message.text} не распознана',
                                 reply_markup=weather_menu)
                bot.register_next_step_handler(message, weatherMenu)
                break
            elif text == 'Ввести город':
                del_markup = ReplyKeyboardRemove(selective=False)
                bot.send_message(message.chat.id, 'Для выхода, наберите слово стоп', reply_markup=del_markup)
                """ stop = ['Стоп', 'СТОП', 'стоп', 'stop', 'STOP', 'Stop']
                @bot.message_handler(content_types=['text'])
                @bot.edited_message_handler(content_types=['text'])
                def handler_command_text(message: Message):
                    while True:
                        if message.text == '1':
                            msg = bot.reply_to(message, 'ВЫХОД', reply_markup=weather_menu)
                            bot.register_next_step_handler(msg, weatherMenu)
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
                                bot.send_message(message.chat.id, config.INFO_NOT_FOUND) """
            else:
                return

    def mainMenu(message: Message):
        text: str = message.text
        if text == 'Погода':
            msg = bot.reply_to(message, 'Выберите город из списка или введите свой', reply_markup=weather_menu)
            bot.register_next_step_handler(msg, weatherMenu)
        elif text == 'Настройки':
            msg = bot.reply_to(message, 'Настройки', reply_markup=config_menu)
            bot.register_next_step_handler(msg, configMenu)
        elif text == 'Убрать меню':
            del_markup = ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, 'Для возврата меню: /menu',
                             reply_markup=del_markup)
        else:
            return

    msg = bot.reply_to(message, "Выберете пункт меню", reply_markup=main_menu)
    bot.register_next_step_handler(msg, mainMenu)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

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

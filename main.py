#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NAME = ПогодныйБот
# BOT NICKNAME = StepTelegramBot
# Autor: Stepan Skriabin
# email: stepan.skrjabin@gmail.com
__version__ = '0.0.9b1'

from telebot import TeleBot
from telebot.types import Message
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ReplyKeyboardRemove
from telebot.types import KeyboardButton
from translitua import translit
from translitua import RussianInternationalPassport1997
import sqlobject as orm

import botconfig
from botsearch import search_weather
from botsearch import replace_name
from models import Users
from models import UsersSettings
from models import CurrentWeather
from models import ForecastWeather
from models import OnecallWeather
from botbase import write_current
from botbase import write_users
from botbase import write_onecall
from botbase import write_forecast


bot = TeleBot(botconfig.TELEGRAM_TOKEN_API)

"""
    Choose the option to connect to the database, where:
    LOCAL_SQLITE: bot_database.db file will be created
    in the local directory
    LOCAL_POSTGRESQL: connection to a local server
    ONLINE_POSTGRESQL: connection will be made to a server hosted
    on the Internet.

    The settings are in the file botconfig.py
"""
connection = orm.connectionForURI(botconfig.LOCAL_SQLITE)
orm.sqlhub.processConnection = connection


# Return information about StepTelegramBot
@bot.message_handler(commands=['start'])
@bot.edited_message_handler(commands=['start'])
def handler_command_start(message: Message):
    bot.send_message(message.chat.id, botconfig.START_MESSAGE,
                     parse_mode='HTML')
    return


# Return help information
@bot.message_handler(commands=['help'])
@bot.edited_message_handler(commands=['help'])
def handler_command_help(message: Message):
    bot.send_message(message.chat.id,
                     botconfig.HELP_MESSAGE.format(__version__),
                     parse_mode='HTML')
    return


# Return version for StepTelegramBot
@bot.message_handler(commands=['register'])
@bot.edited_message_handler(commands=['register'])
def handler_command_version(message: Message):
    bot.send_message(message.chat.id,
                     botconfig.REGISTER_MESSAGE,
                     parse_mode='HTML')
    return

# Registration
@bot.message_handler(commands=['reguser'])
@bot.edited_message_handler(commands=['reguser'])
def handler_command_adduser(message: Message):
    data = [message.from_user.id,
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username,
            message.from_user.language_code,
            message.from_user.is_bot]
    dbquery = Users.select(
        Users.q.userID == message.from_user.id)
    if bool(dbquery.count()):
        bot.send_message(message.chat.id,
                         botconfig.USER_ALREDY_REGISTERED.format(
                             dbquery[0].userName,
                             dbquery[0].userID))
    else:
        write_users(data)
        bot.send_message(message.chat.id,
                         botconfig.USER_IS_REGISTERED.format(
                             message.from_user.username,
                             message.from_user.id))
    return


@bot.message_handler(commands=['deluser'])
@bot.edited_message_handler(commands=['deluser'])
def handler_command_deluser(message: Message):
    dbquery = Users.select(
        Users.q.userID == message.from_user.id)
    if bool(dbquery.count()):
        Users.delete(dbquery[0].id)
        bot.send_message(message.chat.id, botconfig.USER_IS_DELETED.format(
            message.from_user.username,
            message.from_user.id))
    else:
        bot.send_message(message.chat.id, botconfig.USER_NOT_EXIST.format(
            message.from_user.username,
            message.from_user.id))
    return


# Reply markup Keyboard
@bot.message_handler(commands=['menu'])
def markupConfig(message: Message):
    # Main menu
    main_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    mainbtn1 = KeyboardButton('Погода')
    mainbtn2 = KeyboardButton('Настройки')
    main_menu.add(mainbtn1, mainbtn2)
    # Configuration menu
    config_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    configbtn1 = KeyboardButton('Регистрация')
    configbtn2 = KeyboardButton('Удаление')
    configbtn3 = KeyboardButton('Показать настройки')
    configbtn4 = KeyboardButton('Месторасположение')
    configbtn5 = KeyboardButton('Тип прогноза')
    configbtn6 = KeyboardButton('Уведомление')
    configbtn7 = KeyboardButton('Назад в главное меню')
    config_menu.add(configbtn1, configbtn2, configbtn3, configbtn4, configbtn5, configbtn6, configbtn7)
    # City menu
    сity_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    сitybtn1 = KeyboardButton('Указать место')
    сitybtn2 = KeyboardButton('Определить место')
    сitybtn3 = KeyboardButton('Указать долготу')
    сitybtn4 = KeyboardButton('Указать широту')
    сitybtn5 = KeyboardButton('Назад в главное меню')
    сity_menu.add(сitybtn1, сitybtn2, сitybtn3, сitybtn4, сitybtn5)
    # Type of weather
    weather_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    weatherbtn1 = KeyboardButton('Forecast')
    weatherbtn2 = KeyboardButton('Hourly')
    weatherbtn3 = KeyboardButton('Dayli')
    weatherbtn4 = KeyboardButton('Назад в главное меню')
    weather_menu.add(weatherbtn1, weatherbtn2, weatherbtn3, weatherbtn4)
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
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Утром и вечером':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Отключить':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Назад в главное меню':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        else:
            return

    def weatherMenu(message: Message):
        text = message.text
        if text == 'Forecast':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Hourly':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Dayli':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Назад в главное меню':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        else:
            return

    def сityMenu(messaga: Message):
        text = message.text
        if text == 'Указать место':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Определить место':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Указать долготу':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Указать широту':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Назад в главное меню':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        else:
            return

    def configMenu(message: Message):
        text = message.text
        if text == 'Регистрация':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Удаление':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Показать настройки':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Месторасположение':
            msg = bot.reply_to(message, 'ЗАГЛУШКА', reply_markup=сity_menu)
            bot.register_next_step_handler(msg, сityMenu)
        elif text == 'Тип прогноза':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Уведомление':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Назад в главное меню':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        else:
            return

    def mainMenu(message: Message):
        text = message.text
        if text == 'Погода':
            msg = bot.reply_to(message, 'ЗАГЛУШКА')
            bot.register_next_step_handler(msg, markupConfig)
        elif text == 'Настройки':
            msg = bot.reply_to(message, 'Настройки', reply_markup=config_menu)
            bot.register_next_step_handler(msg, configMenu)
        else:
            return

    msg = bot.reply_to(message, "Выберете пункт меню", reply_markup=main_menu)
    bot.register_next_step_handler(msg, mainMenu)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()


@bot.message_handler(commands=['info'])
@bot.edited_message_handler(commands=['info'])
def handler_command_info(message: Message):
    dbquery = UsersSettings.select(
        UsersSettings.q.user == message.from_user.id)
    if bool(dbquery.count()):
        bot.send_message(message.chat.id, botconfig.USER_INFO.format(
            dbquery[0].user,
            dbquery[0].userTown,
            dbquery[0].townLon,
            dbquery[0].townLat,
            dbquery[0].remindTime,
            dbquery[0].remindDay,
            dbquery[0].remindQuantity))
    else:
        bot.send_message(message.chat.id, botconfig.USER_NOT_EXIST.format(
            message.from_user.username,
            message.from_user.id))
    return


@bot.message_handler(commands=['chepetsk'])
@bot.edited_message_handler(commands=['chepetsk'])
def handler_command_chepetsk(message: Message):
    result = search_weather(town='Kirovo-Chepetsk', option='current')
    if result['cod'] == 200:
        write_current(result)
        dbquery = CurrentWeather.select(
            CurrentWeather.q.dateTime == result['dt'])
        bot.send_message(message.chat.id,
                         botconfig.CURRENT_WEATHER_MESSAGE.format(
                             replace_name(dbquery[0].cityName),
                             dbquery[0].weatherDescription,
                             botconfig.EMOJI_DICT[dbquery[0].weatherId],
                             dbquery[0].mainTemp,
                             dbquery[0].mainFeelsLike,
                             dbquery[0].mainPressure,
                             dbquery[0].mainHumidity,
                             dbquery[0].cloudsAll,
                             dbquery[0].windSpeed
                         ), parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, botconfig.INFO_NOT_FOUND)
    return


@bot.message_handler(commands=['kirov'])
@bot.edited_message_handler(commands=['kirov'])
def handler_command_kirov(message: Message):
    result = search_weather(town='Kirov', option='current')
    if result['cod'] == 200:
        write_current(result)
        dbquery = CurrentWeather.select(
            CurrentWeather.q.dateTime == result['dt'])
        bot.send_message(message.chat.id,
                         botconfig.CURRENT_WEATHER_MESSAGE.format(
                             replace_name(dbquery[0].cityName),
                             dbquery[0].weatherDescription,
                             botconfig.EMOJI_DICT[dbquery[0].weatherId],
                             dbquery[0].mainTemp,
                             dbquery[0].mainFeelsLike,
                             dbquery[0].mainPressure,
                             dbquery[0].mainHumidity,
                             dbquery[0].cloudsAll,
                             dbquery[0].windSpeed
                         ), parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, botconfig.INFO_NOT_FOUND)
    return

# Return current weather in fixed city for registred User
@bot.message_handler(commands=['current'])
@bot.edited_message_handler(commands=['current'])
def handler_command_current(message: Message):
    dbquery = Users.select(Users.q.userTown == message.from_user.id)
    if bool(dbquery.count()):
        town = dbquery[0].userTown
        result = search_weather(town, option='current')
        write_current(result)
    else:
        bot.send_message(
            message.chat.id, botconfig.FUNCTION_FOR_REGISTERED_USER)
        return
    dbquery = CurrentWeather.selectBy(
        dateTime=result['dt'], cityName=town)
    if bool(dbquery.count()):
        bot.send_message(message.chat.id,
                         botconfig.CURRENT_WEATHER_MESSAGE.format(
                             replace_name(dbquery[0].cityName),
                             dbquery[0].weatherDescription,
                             botconfig.EMOJI_DICT[dbquery[0].weatherId],
                             dbquery[0].mainTemp,
                             dbquery[0].mainFeelsLike,
                             dbquery[0].mainPressure,
                             dbquery[0].mainHumidity,
                             dbquery[0].cloudsAll,
                             dbquery[0].windSpeed
                         ), parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, botconfig.INFO_NOT_FOUND)
    return


# Return forecast weather in fixed city for registred User
@bot.message_handler(commands=['forecast'])
@bot.edited_message_handler(commands=['forecast'])
def handler_command_forecast(message: Message):
    dbquery = Users.select(Users.q.userId == message.from_user.id)
    if bool(dbquery.count()):
        town = dbquery[0].userTown
        result = search_weather(town, option='forecast')
        write_forecast(result)
    else:
        bot.send_message(
            message.chat.id, botconfig.FUNCTION_FOR_REGISTERED_USER)
        return
    dbquery = ForecastWeather.selectBy(
        dateTime=result['dt'], cityName=town)
    if bool(dbquery.count()):
        bot.send_message(message.chat.id,
                         botconfig.FORECAST_WEATHER_MESSAGE.format(
                             replace_name(dbquery[0].cityName),
                             dbquery[0].weatherDescription,
                             botconfig.EMOJI_DICT[dbquery[0].weatherId],
                             dbquery[0].mainTemp,
                             dbquery[0].mainFeelsLike,
                             dbquery[0].mainPressure,
                             dbquery[0].mainHumidity,
                             dbquery[0].cloudsAll,
                             dbquery[0].windSpeed
                         ), parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, botconfig.INFO_NOT_FOUND)
    return


# Return onecall weather in fixed city for registred User
@bot.message_handler(commands=['onecall'])
@bot.edited_message_handler(commands=['onecall'])
def handler_command_onecall(message: Message):
    dbquery = Users.select(Users.q.userId == message.from_user.id)
    if bool(dbquery.count()):
        lon = dbquery[0].userTownLon
        lat = dbquery[0].userTownLat
        town = dbquery[0].userTown
        result = search_weather(town, option='onecall', lon=lon, lat=lat)
        write_onecall(result)
    else:
        bot.send_message(
            message.chat.id, botconfig.FUNCTION_FOR_REGISTERED_USER)
        return
    dbquery = OnecallWeather.selectBy(
        dateTime=result['dt'], lon=lon, lat=lat)
    if bool(dbquery.count()):
        bot.send_message(message.chat.id,
                         botconfig.ONECALL_WEATHER_MESSAGE.format(
                             replace_name(dbquery[0].cityName),
                             dbquery[0].weatherDescription,
                             botconfig.EMOJI_DICT[dbquery[0].weatherId],
                             dbquery[0].mainTemp,
                             dbquery[0].mainFeelsLike,
                             dbquery[0].mainPressure,
                             dbquery[0].mainHumidity,
                             dbquery[0].cloudsAll,
                             dbquery[0].windSpeed
                         ), parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, botconfig.INFO_NOT_FOUND)
    return


# Return weather from city
@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def handler_command_text(message: Message):
    town = translit(message.text, RussianInternationalPassport1997)
    result = search_weather(town, option='current')
    if result['cod'] == 200:
        write_current(result)
        dbquery = CurrentWeather.select(
            CurrentWeather.q.dateTime == result['dt'])
        bot.send_message(message.chat.id,
                         botconfig.CURRENT_WEATHER_MESSAGE.format(
                             replace_name(dbquery[0].cityName),
                             dbquery[0].weatherDescription,
                             botconfig.EMOJI_DICT[dbquery[0].weatherId],
                             dbquery[0].mainTemp,
                             dbquery[0].mainFeelsLike,
                             dbquery[0].mainPressure,
                             dbquery[0].mainHumidity,
                             dbquery[0].cloudsAll,
                             dbquery[0].windSpeed
                         ), parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, botconfig.INFO_NOT_FOUND)
    return


print('StepTelegramBot is running')
# RUN
bot.polling(timeout=900)

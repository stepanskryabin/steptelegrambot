#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NAME = ПогодныйБот
# BOT NICKNAME = StepTelegramBot
# Autor: Stepan Skriabin
# email: stepan.skrjabin@gmail.com
__version__ = '0.0.9b1'

from telebot import TeleBot
from telebot.types import Message
from telebot.types import InlineQueryResultArticle
from telebot.types import InputTextMessageContent
from translitua import translit
from translitua import RussianInternationalPassport1997
import sqlobject as orm

import botconfig
from botsearch import search_weather
from botsearch import replace_name
from models import Users
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
    LOCAL_SQLITE: the bot_database.db file will be created
    in the local directory
    LOCAL_POSTGRESQL: a connection to a local server will be made
    ONLINE_POSTGRESQL: a connection will be made to a server hosted
    on the Internet.

    The settings are in the file botconfig.py
"""
connection = orm.connectionForURI(botconfig.ONLINE_POSTGRESQL)
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
        Users.q.userID == data[0])
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


@bot.message_handler(commands=['chepetsk'])
@bot.edited_message_handler(commands=['chepetsk'])
def handler_command_chepetsk(message: Message):
    result = search_weather(town='Kirovo-Chepetsk', option='current')
    if result['cod'] == 200:
        print(result['sys']['country'])
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


# Inline mode search weather in Kirov or Kirovo-Chepetsk
@bot.inline_handler(lambda query: query.query in ['Ки', 'Ki', 'ки', 'ki'])
def query_text(inline_query):
    try:
        kirov = InlineQueryResultArticle(
            '1', 'Киров', InputTextMessageContent('Киров'))
        kirovochepetsk = InlineQueryResultArticle(
            '2', 'Кирово-Чепецк', InputTextMessageContent('Кирово-Чепецк'))
        bot.answer_inline_query(inline_query.id, [kirov, kirovochepetsk])
    except Exception as e:
        print(e)


# Echo replay
# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)

print('StepTelegramBot is running')
# RUN
bot.polling(timeout=900)

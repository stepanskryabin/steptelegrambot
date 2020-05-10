#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NAME = ПогодныйБот
# NICKNAME = StepTelegramBot
# Autor: Stepan Skriabin
# email: stepan.skrjabin@gmail.com
__version__ = '0.0.8'

import os

from telebot import TeleBot
from telebot.types import Message
from telebot.types import InlineQueryResultArticle
from telebot.types import InputTextMessageContent
from translitua import translit
from translitua import RussianInternationalPassport1997

import botconfig
from botsearch import SearchWeather
from models import Users
from models import CurrentWeather
from models import ForecastWeather
from models import OnecallWeather
from botbase import write_current_weather
from botbase import write_users
from botbase import write_onecall


bot = TeleBot(os.getenv('BOT_API'))

# Create a new SearchWeather object
w = SearchWeather()

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
        Users.q.userId == data[0])
    if bool(dbquery.count()):
        bot.send_message(message.chat.id,
                         botconfig.USER_ALREDY_REGISTERED.format(
                             dbquery[0].userName,
                             dbquery[0].userId))
    else:
        bot.send_message(message.chat.id, botconfig.REGISTER_PROCEED)
        write_users(data)
        bot.send_message(message.chat.id,
                         botconfig.USER_IS_REGISTERED.format(
                             dbquery[0].userName,
                             dbquery[0].userId))
    return


@bot.message_handler(commands=['deluser'])
@bot.edited_message_handler(commands=['deluser'])
def handler_command_deluser(message: Message):
    dbquery = Users.select(
        Users.q.userId == message.from_user.id)
    if bool(dbquery.count()):
        Users.delete(dbquery[0].id)
        bot.send_message(message.chat.id, botconfig.USER_IS_DELETED.format(
            dbquery[0].userName,
            dbquery[0].userId))
    else:
        bot.send_message(message.chat.id, botconfig.USER_NOT_EXIST.format(
            dbquery[0].userName,
            dbquery[0].userId))
    return


@bot.message_handler(commands=['chepetsk'])
@bot.edited_message_handler(commands=['chepetsk'])
def handler_command_chepetsk(message: Message):
    check_weather = w.check_current_weather(town='Kirovo-Chepetsk')
    write_current_weather(check_weather)
    dbquery = CurrentWeather.select(
        CurrentWeather.q.dateTime == check_weather['dt'])
    if bool(dbquery.count()):
        bot.send_message(message.chat.id,
                         botconfig.WEATHER_MESSAGE.format(
                             dbquery[0].cityName,
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


# Return weather in fixed city Kirov
@bot.message_handler(commands=['kirov'])
@bot.edited_message_handler(commands=['kirov'])
def handler_command_kirov(message: Message):
    check_weather = w.check_forecast(town='Kirov')
    write_current_weather(check_weather)
    dbquery = CurrentWeather.select(
        CurrentWeather.q.dateTime == check_weather['dt'])
    if bool(dbquery.count()):
        bot.send_message(message.chat.id,
                         botconfig.WEATHER_MESSAGE.format(
                             dbquery[0].cityName,
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
        check_weather = w.check_current_weather(town)
        write_current_weather(check_weather)
    else:
        bot.send_message(
            message.chat.id, botconfig.FUNCTION_FOR_REGISTERED_USER)
        return
    dbquery = CurrentWeather.selectBy(
        dateTime=check_weather['dt'], cityName=town)
    if bool(dbquery.count()):
        bot.send_message(message.chat.id,
                         botconfig.WEATHER_MESSAGE.format(
                             dbquery[0].cityName,
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
def handler_command_cforecast(message: Message):
    dbquery = Users.select(Users.q.userId == message.from_user.id)
    if bool(dbquery.count()):
        town = dbquery[0].userTown
        check_weather = w.check_forecast(town)
        write_current_weather(check_weather)
    else:
        bot.send_message(
            message.chat.id, botconfig.FUNCTION_FOR_REGISTERED_USER)
        return
    dbquery = ForecastWeather.selectBy(
        dateTime=check_weather['dt'], cityName=town)
    if bool(dbquery.count()):
        bot.send_message(message.chat.id,
                         botconfig.FORECAST_WEATHER_MESSAGE.format(
                             dbquery[0].cityName,
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
        check_weather = w.check_onecall(lon, lat)
        write_onecall(check_weather)
    else:
        bot.send_message(
            message.chat.id, botconfig.FUNCTION_FOR_REGISTERED_USER)
        return
    dbquery = OnecallWeather.selectBy(
        dateTime=check_weather['dt'], lon=lon, lat=lat)
    if bool(dbquery.count()):
        bot.send_message(message.chat.id,
                         botconfig.ONECALL_WEATHER_MESSAGE.format(
                             dbquery[0].cityName,
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
    city_name = translit(message.text, RussianInternationalPassport1997)
    check_weather = w.check_current_weather(town=city_name)
    write_current_weather(check_weather)
    dbquery = CurrentWeather.select(
        CurrentWeather.q.dateTime == check_weather['dt'])
    if bool(dbquery.count()):
        bot.send_message(message.chat.id,
                         botconfig.WEATHER_MESSAGE.format(
                             dbquery[0].cityName,
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

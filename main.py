#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot.types import Message
import config
import requests

# NAME = POCO
# NICKNAME = StepTelegramBot

# Город
TOWN_ID: str = 'Kirovo-Chepetsk,RU'
# передача токена телеграм боту
bot = telebot.TeleBot(config.TOKEN)
# Урл куда бот обращается за информацией о погоде
url: str = 'https://api.openweathermap.org/data/2.5/weather?'
# 
town = TOWN_ID
# АПИ токен для доступа к данным сайта openweathermap.org
token = config.TOKEN_WEATHER

USERS = set()
# Константа перевода давления из паскалей в милиметры ртутного столба
const_mm_hg: float = 7.5006E-3


# Функция возвращает json-объект с информацией о погоде в заданном городе
def return_all_weather(weather_url, weather_town, weather_token):
    response = requests.get(weather_url, params={'q': weather_town, 'appid': weather_token, 'units': 'metric'})
    return response.json()


# date = return_all_weather(url, town, token)


@bot.message_handler(commands=['start'])
@bot.edited_message_handler(commands=['start'])
def command_handler(message: Message):
    # sti = open(config.W_STICKER, 'rb')
    # bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Привет, я Погодный бот! Набери help чтобы узнать что я могу")
    return


@bot.message_handler(commands=['help'])
@bot.edited_message_handler(commands=['help'])
def command_handler(message: Message):
    if message.location is not None:
        bot.reply_to(message, f'Этот бот помогает узнать погоду в городе {message.location}\n'
                               'Введите ключевые слова: <b>погода</b>, <b>влажность</b> или <b>давление</b>'
                               ' и я дам вам ответ', parse_mode='HTML')
    else:
        bot.reply_to(message, f'Этот бот помогает узнать погоду в вашем городе \n'
                               'Введите ключевые слова: <b>погода</b>, <b>влажность</b> или <b>давление</b>'
                               ' и я дам вам ответ', parse_mode='HTML')
    return


# Обработчик сообщения с командами
@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def command_handler(message: Message):
    date = return_all_weather(url, town, token)
    if 'погода' in message.text:
        bot.reply_to(message, f"Сейчас температура <b>{date['main']['temp']}</b> градуса. \
        Чувствуется как <b>{date['main']['feels_like']}</b> градуса", parse_mode='HTML')
    elif 'давление' in message.text:
        pa: int = date['main']['pressure']
        mm_hg = (pa * 100) * const_mm_hg
        bot.reply_to(message, f"Сейчас давление <b>{int(mm_hg)} мм.рт.ст</b>", parse_mode='HTML')
    elif 'влажность' in message.text:
        bot.reply_to(message, f"Сейчас влажность <b>{date['main']['humidity']} %</b>", parse_mode='HTML')
    elif 'настроение' in message.text:
        bot.reply_to(message, f"Сейчас настроение - <b>{date['weather']['0']['description']}</b>", parse_mode='HTML')
    else:
        bot.reply_to(message, "Нет! Нужно ввести: <b>погода</b>, <b>влажность</b> или <b>давление</b>", parse_mode='HTML')
    return


# def send_content_message(message: Message):
#     # if 'Я хороший' in message.text:
#     #     bot.reply_to(message, 'Степан хороший!')
#     # print('Message==', message)
#     reply: str = ''
#     if message.from_user.id in USERS:
#         reply += f"{message.from_user.first_name}, hello again"
#         bot.reply_to(message, reply)
#     else:
#         bot.reply_to(message, 'Я тебя вижу в первый раз')
#     USERS.add(message.from_user.id)
#     # print('USERS==', USERS)


@bot.message_handler(content_types=['sticker'])
def sticker_handler(message: Message):
    bot.send_sticker(message.chat.id, config.STICKER_ID)
    return


# @bot.inline_handler(lambda query: query.query == 'weather')
# def query_text(inline_query):
#     try:
#         r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
#         r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
#         bot.answer_inline_query(inline_query.id, [r, r2])
#     except Exception as e:
#         print(e)


# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


# RUN
bot.polling(timeout=10)

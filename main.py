#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NAME = ПогодныйБот
# NICKNAME = StepTelegramBot
# Autor: Stepan Skriabin
# email: stepan.skrjabin@gmail.com
__version__ = '0.0.7'

import os

from telebot import TeleBot
from telebot.types import Message
from telebot.types import InlineQueryResultArticle
from telebot.types import InputTextMessageContent
from translitua import translit
from translitua import RussianInternationalPassport1997

import botconfig
from botsearch import SearchWeather
from botbase import Users


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
    table_users = Users
    if bool(table_users.tableExists()) is False:
        table_users.createTable()
    else:
        pass
    is_user_register = table_users.select(
        Users.q.userId == message.from_user.id)
    check = bool(is_user_register.count())
    if check is True:
        bot.send_message(
            message.chat.id, f'Пользователь: {message.from_user.username} '
            f'с ID {message.from_user.id} уже зарегистрирован.')
    elif check is False:
        table_users(userId=message.from_user.id,
                    userFirstname=message.from_user.first_name,
                    userLastname=message.from_user.last_name,
                    userName=message.from_user.username,
                    languageCode=message.from_user.language_code,
                    isBot=message.from_user.is_bot)
        bot.send_message(
            message.chat.id, f'Пользователь: {message.from_user.username} '
            f'с ID: {message.from_user.id} создан.')
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так')


@bot.message_handler(commands=['deluser'])
@bot.edited_message_handler(commands=['deluser'])
def handler_command_deluser(message: Message):
    table_users = Users
    if table_users.tableExists() is False:
        pass
    else:
        is_user_register = table_users.select(
            Users.q.userId == message.from_user.id)
        check = bool(is_user_register.count())
        if check is True:
            table_users.delete(is_user_register.min('id'))
            bot.send_message(message.chat.id,
                             f'Пользователь: {message.from_user.username} '
                             f'с ID: {message.from_user.id} удалён.')
        elif check is False:
            bot.send_message(message.chat.id,
                             f'Пользователя: {message.from_user.username} '
                             f'с ID: {message.from_user.id} не существует.')
        else:
            bot.send_message(message.chat.id, 'Что-то пошло не так')


@bot.message_handler(commands=['chepetsk'])
@bot.edited_message_handler(commands=['chepetsk'])
def handler_command_chepetsk(message: Message):
    w.check_weather(town='Kirovo-Chepetsk')
    bot.send_message(message.chat.id, f"Сейчас в {w.city_name()} <b><i>{w.description()}</i></b> {w.insert_emoji()} \n"
                                      f"Температура: <b>{w.temp()} C</b>. \n"
                                      f"Чувствуется как: <b>{w.feels()} C</b>. \n"
                                      f"Давление: <b>{w.pressure()} мм.рт.ст.</b> \n"
                                      f"Влажность: <b>{w.humidity()} %</b> \n"
                                      f"Облачность: <b>{w.clouds()} %</b> \n"
                                      f"Скорость ветра: <b>{w.speed_wing()} метров в сек.</b>", parse_mode='HTML')
    return


# Return weather in fixed city Kirov
@bot.message_handler(commands=['kirov'])
@bot.edited_message_handler(commands=['kirov'])
def handler_command_kirov(message: Message):
    w.check_weather(town='Kirov')
    bot.send_message(message.chat.id, f"Сейчас в {w.city_name()} <b><i>{w.description()}</i></b> {w.insert_emoji()} \n"
                                      f"Температура: <b>{w.temp()} C</b>. \n"
                                      f"Чувствуется как: <b>{w.feels()} C</b>. \n"
                                      f"Давление: <b>{w.pressure()} мм.рт.ст.</b> \n"
                                      f"Влажность: <b>{w.humidity()} %</b> \n"
                                      f"Облачность: <b>{w.clouds()} %</b> \n"
                                      f"Скорость ветра: <b>{w.speed_wing()} метров в сек.</b>", parse_mode='HTML')
    return


# Return weather from city
@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def handler_command_text(message: Message):
    city_name = translit(message.text, RussianInternationalPassport1997)
    w.check_weather(town=city_name)
    if w.result() == 200:
        bot.send_message(message.chat.id,
                         f"Сейчас в {w.city_name()} <b><i>{w.description()}</i></b> {w.insert_emoji()} \n"
                         f"Температура: <b>{w.temp()} C</b>. \n"
                         f"Чувствуется как: <b>{w.feels()} C</b>. \n"
                         f"Давление: <b>{w.pressure()} мм.рт.ст.</b> \n"
                         f"Влажность: <b>{w.humidity()} %</b> \n"
                         f"Облачность: <b>{w.clouds()} %</b> \n"
                         f"Скорость ветра: <b>{w.speed_wing()} метров в сек.</b>", parse_mode='HTML')
    elif w.result() == '404':
        bot.send_message(
            message.chat.id, f"\U0001F6AB Такой город <s> не существует </s>. Возможно вы допустили ошибку?", parse_mode='HTML')
    else:
        bot.send_message(
            message.chat.id, f"кТО Здесь? \U0001F628", parse_mode='HTML')
    return


# Return sticker
@bot.message_handler(content_types=['sticker'])
def handler_sticker(message: Message):
    bot.send_sticker(message.chat.id, botconfig.STICKER_ID)
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

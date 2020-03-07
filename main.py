#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NAME = ПогодныйБот
# NICKNAME = StepTelegramBot
# Autor: Stepan Skriabin
# email: stepan.skrjabin@gmail.com

#import logging
import telebot
from telebot.types import Message
import config
import TOKEN
from translitua import translit, RussianInternationalPassport1997
from searching_modul import SearchWeather


# TODO Porting function 'search' and 'choose another city' in module
# Create a new Telegram Bot object
bot = telebot.TeleBot(TOKEN.BOT)

# Configuring the logging module
#logging.basicConfig(filename=config.FILENAME, filemode=config.FILEMODE, format=config.FORMAT_MESSAGE, datefmt=config.DATE_FORMAT, level=config.MESSAGE_LEVEL)

# Create a new SearchWeather object
w = SearchWeather()

# List of users id (from telegram)
# TODO added collection of Users ID and Users configuration
# USERS = set()

# Return information about StepTelegramBot
@bot.message_handler(commands=['start'])
@bot.edited_message_handler(commands=['start'])
def command_handler(message: Message):
    # Insert sticker in message text
    # sti = open(config.W_STICKER, 'rb')
    # bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Привет, я <b>Погодный бот!</b>\n"
                                      "Набери имя города и я поищу информацию о погоде в нём.\n"
                                      "Если нужна более подробная информация жми /help", parse_mode='HTML')
    return


# Return help information
@bot.message_handler(commands=['help'])
@bot.edited_message_handler(commands=['help'])
def command_handler(message: Message):
    if message.location is not None:
        bot.send_message(message.chat.id, f'Этот бот помогает узнать погоду в городе {message.location}\n'
                                          'Введите название города, непример: Киров и я дам вам ответ',
                         parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, f'Этот бот помогает узнать погоду в вашем городе \n'
                                          'Введите название города, непример: Москва и я дам ответ.\n'
                                          'Ещё у меня есть встроенные команды для поиска погоды в Кирове и Кирово-Чепецке.\n'
                                          'Просто набери команду /chepetsk или /kirov', parse_mode='HTML')
    return


# Return version for StepTelegramBot
@bot.message_handler(commands=['version'])
@bot.edited_message_handler(commands=['version'])
def command_handler(message: Message):
#    logging.debug(f'Bot version request={w.version()}')
    bot.send_message(message.chat.id, f"Версия бота: {w.version()}", parse_mode='HTML')
    return


# Return weather in fixed city Kirovo-Chepetsk
# TODO change this function
@bot.message_handler(commands=['chepetsk'])
@bot.edited_message_handler(commands=['chepetsk'])
def command_handler(message: Message):
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
# TODO change this function
@bot.message_handler(commands=['kirov'])
@bot.edited_message_handler(commands=['kirov'])
def command_handler(message: Message):
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
def command_handler(message: Message):
    city_name = translit(message.text, RussianInternationalPassport1997)
#    logging.debug(f'City name={city_name}')
    w.check_weather(town=city_name)
#    logging.debug(f'Value w.result={w.result()}')
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
        bot.send_message(message.chat.id, f"\U0001F6AB Такой город <s>не существует</s>. Возможно вы допустили ошибку?",
                         parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, f"кТО Здесь? \U0001F628", parse_mode='HTML')
    return


# Return sticker
@bot.message_handler(content_types=['sticker'])
def sticker_handler(message: Message):
    bot.send_sticker(message.chat.id, config.STICKER_ID)
    return


# Inline mode search weather in Kirov or Kirovo-Chepetsk
@bot.inline_handler(lambda query: query.query in ['Ки', 'Ki', 'ки', 'ki'])
def query_text(inline_query):
    try:
        kirov = telebot.types.InlineQueryResultArticle('1', 'Киров', telebot.types.InputTextMessageContent('Киров'))
        kirovochepetsk = telebot.types.InlineQueryResultArticle('2', 'Кирово-Чепецк', telebot.types.InputTextMessageContent('Кирово-Чепецк'))
        bot.answer_inline_query(inline_query.id, [kirov, kirovochepetsk])
    except Exception as e:
        print(e)


# Echo replay
# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


# RUN
bot.polling(timeout=300)

# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Search weather on the openweathermap.org

import requests
from translitua import translit
from translitua import RussianInternationalPassport1997
import app.config as config


def search_weather(town, option, lon=None, lat=None):
    """
    town: string type, mandatory parameter
    option: string type, mandatory parameter
    lon: int type, default=None
    lat: int type, default=None
    """
    town = translit(town, RussianInternationalPassport1997)
    url = {"current": 'https://api.openweathermap.org/data/2.5/weather?',
           "onecall": 'https://api.openweathermap.org/data/2.5/onecall?',
           "forecast": 'https://api.openweathermap.org/data/2.5/forecast?'
           }
    token = config.WEATHER_TOKEN_API
    parametres = {'current':
                  {'q': town,
                   'appid': token,
                   'units': 'metric',
                   'lang': 'RU'},
                  'forecast':
                  {'q': town,
                   'appid': token,
                   'units': 'metric',
                   'lang': 'RU'},
                  'onecall':
                  {'lat': lat,
                   'lon': lon,
                   'appid': token,
                   'units': 'metric',
                   'lang': 'RU'}
                  }
    response = requests.get(url[option], params=parametres[option])
    data = response.json()
    return data


def replace_name(word):
    """
        Return city name with replace end of word
        word: string type
    """
    if word[-2:] == 'ий':
        new_word = word.replace(word[-2:], 'ом')
    elif word[-1:] in ['а', 'o', 'у', 'ъ', 'ь', 'ю', 'э', 'й', 'я']:
        new_word = word.replace(word[-1:], 'е')
    elif word[-1:] == 'ь':
        new_word = word.replace(word[-1:], 'и')
    elif word[-1:] in ['ы', 'и']:
        new_word = word.replace(word[-1:], 'ах')
    elif word[-1:] in ['в', 'к', 'р', 'н', 'с', 'т',
                       'л', 'ш', 'щ', 'з', 'х', 'п',
                       'д', 'ж', 'ч', 'м', 'б', 'г'
                       ]:
        new_word = word + 'е'
    else:
        new_word = word
    return new_word


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

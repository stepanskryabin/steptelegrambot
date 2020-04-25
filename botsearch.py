#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Search weather on the openweathermap.org

import requests
import os
import config
# import botbase


class SearchWeather:
    """
    Send requests from openweathermap.org and
    get JSON-file with information
    """

    def __init__(self):
        self.url: str = 'https://api.openweathermap.org/data/2.5/weather?'
        self.token: str = os.getenv('WEATHER_API')
        self.response = ''
        self.data = {}
        self.last_word = 0
        self.quantity_word = 0

    def check_weather(self, town=None):
        self.town: str = town
        self.response = requests.get(self.url,
                                     params={'q': self.town,
                                             'appid': self.token,
                                             'units': 'metric',
                                             'lang': 'RU'
                                             })
        self.data = self.response.json()

    # Return error code
    def result(self):
        search_result = self.data['cod']
        return search_result

    # Return city name with replace end of word
    def city_name(self):
        word: str = self.data['name']
        if word[-2:] == 'ий':
            new_word: str = word.replace(word[-2:], 'ом')
        elif word[-1:] in ['а', 'o', 'у', 'ъ', 'ь', 'ю', 'э', 'й', 'я']:
            new_word: str = word.replace(word[-1:], 'е')
        elif word[-1:] == 'ь':
            new_word: str = word.replace(word[-1:], 'и')
        elif word[-1:] in ['ы', 'и']:
            new_word: str = word.replace(word[-1:], 'ах')
        elif word[-1:] in ['в', 'к', 'р', 'н', 'с', 'т',
                           'л', 'ш', 'щ', 'з', 'х', 'п',
                           'д', 'ж', 'ч', 'м', 'б', 'г'
                           ]:
            new_word: str = word + 'е'
        else:
            new_word: str = word
        return new_word

    def description(self):
        weather_description = self.data['weather'][0]['description']
        return weather_description

    def temp(self):
        main_temp = self.data['main']['temp']
        return main_temp

    def feels(self):
        feels_like = self.data['main']['feels_like']
        return feels_like

    # Return pressure and converting Pascal to mercury pole millimeters
    def pressure(self):
        pa: int = self.data['main']['pressure']
        mpm = (pa * 100) * config.CONSTANT_PA_TO_MPM
        return int(mpm)

    def humidity(self):
        main_humidity = self.data['main']['humidity']
        return main_humidity

    def speed_wing(self):
        speed = self.data['wind']['speed']
        return speed

    def clouds(self):
        all_clouds = self.data['clouds']['all']
        return all_clouds

    def version(self):
        return self.development

    # Return code of emoji from weather description
    def insert_emoji(self):
        icon_name = self.data['weather'][0]['id']
        dict = {
            200: '\U00002744',
            201: '\U000026A1',
            202: '\U000026A1',
            210: '\U000026C5',
            211: '\U000026C5',
            212: '\U000026C5',
            221: '\U000026C5',
            230: '\U000026A1',
            231: '\U000026A1',
            232: '\U000026A1',
            300: '\U00002614',
            301: '\U00002614',
            302: '\U00002614',
            310: '\U00002614',
            311: '\U00002614',
            312: '\U00002614',
            313: '\U00002614',
            314: '\U00002614',
            321: '\U00002614',
            500: '\U0001F302',
            501: '\U0001F302',
            502: '\U0001F302',
            503: '\U0001F302',
            504: '\U0001F302',
            511: '\U00002614',
            520: '\U00002614',
            521: '\U00002614',
            522: '\U00002614',
            531: '\U00002614',
            600: '\U00002744',
            601: '\U00002744',
            602: '\U00002744',
            611: '\U00002744',
            612: '\U00002744',
            613: '\U00002744',
            614: '\U00002744',
            615: '\U00002744',
            616: '\U00002744',
            620: '\U00002744',
            621: '\U00002744',
            622: '\U00002744',
            701: '\U0001F301',
            711: '\U0001F301',
            712: '\U0001F301',
            721: '\U0001F301',
            731: '\U0001F301',
            741: '\U0001F301',
            751: '\U0001F301',
            761: '\U0001F301',
            762: '\U0001F301',
            771: '\U0001F301',
            781: '\U0001F300',
            800: '\U000026C5',
            801: '\U00002601',
            802: '\U00002601',
            803: '\U000026C5',
            804: '\U00002601'
        }
        return dict[int(icon_name)]


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

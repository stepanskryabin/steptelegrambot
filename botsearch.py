#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Search weather on the openweathermap.org

import requests
import os

import botconfig
from botbase import CityList


class SearchWeather:
    """
    Send requests from openweathermap.org and
    get JSON-file with information
    """

    def __init__(self):
        self.url: str = 'https://api.openweathermap.org/data/2.5/'
        self.api_call_weather = 'weather?'
        self.api_call_hourly = 'onecall?'
        self.token: str = os.getenv('WEATHER_API')
        self.data = {}
        self.last_word = 0
        self.quantity_word = 0

    def check_weather(self, town='Moscow'):
        """
        The function forms and sends a request to the site,
        the result of the function is JSON-object.
        """
        url = self.url + self.api_call_weather
        response = requests.get(url,
                                params={'q': town,
                                        'appid': self.token,
                                        'units': 'metric',
                                        'lang': 'RU'
                                        })
        data = response.json()
        return data

    def check_hourly_and_daily(self, town='Moscow'):
        table = CityList.select(CityList.q.name == town)
        row_id = int(table.min())
        column = CityList.get(row_id)
        lon = column.lon
        lat = column.lat
        url = self.url + self.api_call_hourly
        response = requests.get(url, params={'lon': lon,
                                             'lat': lat,
                                             'appid': self.token})
        data = response.json()
        return data

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
        mpm = (pa * 100) * botconfig.CONSTANT_PA_TO_MPM
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

    # Return code of emoji from weather description
    def insert_emoji(self):
        icon_name = self.data['weather'][0]['id']
        emoji = botconfig.EMOJI_DICT
        return emoji[int(icon_name)]


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

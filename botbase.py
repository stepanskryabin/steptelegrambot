#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Create and work with database

import sqlobject as orm
import botconfig

from models import Users
from models import CurrentWeather
from models import ForecastWeather


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


def write_users(*args):
    data = args
    Users(userId=data[0],
          userFirstname=data[1],
          userLastname=data[2],
          userName=data[3],
          languageCode=data[4],
          isBot=data[5])


def write_current(**kwargs):
    data = kwargs
    CurrentWeather(
        cityId=data['id'],
        cityName=data['name'],
        lon=data['coord']['lon'],
        lat=data['coord']['lat'],
        dateTime=data['dt'],
        weatherId=data['weather'][0]['id'],
        weatherMain=data['weather'][0]['main'],
        weatherDescription=data['weather'][0]['description'],
        weatherIcon=data['weather'][0]['icon'],
        base=data['base'],
        mainTemp=data['main']['temp'],
        mainFeelsLike=data['main']['feels_like'],
        mainTempMin=data['main']['temp_min'],
        mainTempMax=data['main']['temp_max'],
        mainPressure=data['main']['pressure'],
        mainHumidity=data['main']['humidity'],
        visibility=data['visibility'],
        windSpeed=data['wind']['speed'],
        cloudsAll=data['clouds']['all'],
        sysType=data['sys']['type'],
        sysId=data['sys']['id'],
        sysCountry=data['sys']['country'],
        sysSunrise=data['sys']['sunrise'],
        sysSunset=data['sys']['sunset'],
        timezone=data['timezone']
    )


def write_forecast(**kwargs):
    data = kwargs
    ForecastWeather.createTable(ifNotExist=True)
    if data['cod'] == 200:
        for i in range(40):
            ForecastWeather(cityId=data['city']['id'],
                            cityName=data['city']['name'],
                            lon=['coord']['lon'],
                            lat=['coord']['lat'],
                            country=['city']['country'],
                            timezone=['city']['timezone'],
                            sunrise=['city']['sunrise'],
                            sunset=['city']['sunset'],
                            dateTime=['list'][i]['dt'],
                            dateTimeText=['list'][i]['dt_txt'],
                            mainTemp=['list'][i]['main']['temp'],
                            mainFeelsLike=['list'][i]['main']['feels_like'],
                            mainTempMin=['list'][i]['main']['temp_min'],
                            mainTempMax=['list'][i]['main']['temp_max'],
                            mainPressure=['list'][i]['main']['pressure'],
                            mainSeaLevel=['list'][i]['main']['sea_level'],
                            mainGroundLevel=['list'][i]['main']['grnd_level'],
                            mainHumidity=['list'][i]['main']['humidity'],
                            mainTempkf=['list'][i]['main']['temp_k'],
                            weatherId=['list'][i]['weather']['id'],
                            weatherMain=['list'][i]['weather']['main'],
                            weatherDescription=[
                                'list'][i]['weather']['description'],
                            weatherIcon=['list'][i]['weather']['icon'],
                            cloudsAll=['list'][i]['clouds']['all'],
                            windSpeed=['list'][i]['wind']['speed'],
                            windDeg=['list'][i]['wind']['deg'],
                            sysPod=['list'][i]['sys']['pod'])
        print('write_current_weather = OK')
    elif data == '400':
        print('No such city has been found')


def write_onecall():
    pass


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

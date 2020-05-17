#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Create and work with database

from models import Users
from models import CurrentWeather
from models import ForecastWeather


def write_users(data):
    Users(userID=data[0],
          userFirstName=data[1],
          userLastName=data[2],
          userName=data[3],
          languageCode=data[4],
          isBot=data[5]
          )


def write_current(data):
    CurrentWeather(
        cityId=data['id'],
        cityName=data['name'],
        lon=data['coord']['lon'],
        lat=data['coord']['lat'],
        country=data['sys']['country'],
        timezone=data['timezone'],
        sunrise=data['sys']['sunrise'],
        sunset=data['sys']['sunset'],
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
        windSpeed=data['wind']['speed'],
        windDeg=data['wind']['deg'],
        cloudsAll=data['clouds']['all'],
        )


def write_forecast(**kwargs):
    data = kwargs
    for i in range(40):
        ForecastWeather(cityId=data['city']['id'],
                        cityName=data['city']['name'],
                        lon=data['coord']['lon'],
                        lat=data['coord']['lat'],
                        country=data['city']['country'],
                        timezone=data['city']['timezone'],
                        sunrise=data['city']['sunrise'],
                        sunset=data['city']['sunset'],
                        dateTime=data['list'][i]['dt'],
                        dateTimeText=data['list'][i]['dt_txt'],
                        mainTemp=data['list'][i]['main']['temp'],
                        mainFeelsLike=data['list'][i]['main']['feels_like'],
                        mainTempMin=data['list'][i]['main']['temp_min'],
                        mainTempMax=data['list'][i]['main']['temp_max'],
                        mainPressure=data['list'][i]['main']['pressure'],
                        mainSeaLevel=data['list'][i]['main']['sea_level'],
                        mainGroundLevel=data['list'][i]['main']['grnd_level'],
                        mainHumidity=data['list'][i]['main']['humidity'],
                        mainTempkf=data['list'][i]['main']['temp_k'],
                        weatherId=data['list'][i]['weather']['id'],
                        weatherMain=data['list'][i]['weather']['main'],
                        weatherDescription=data[
                        'list'][i]['weather']['description'],
                        weatherIcon=data['list'][i]['weather']['icon'],
                        cloudsAll=data['list'][i]['clouds']['all'],
                        windSpeed=data['list'][i]['wind']['speed'],
                        windDeg=data['list'][i]['wind']['deg'],
                        sysPod=data['list'][i]['sys']['pod']
                        )


def write_onecall():
    pass


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

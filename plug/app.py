#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Create and work with database

import json

from models import Users
from models import CurrentWeather
from models import ForecastWeather
from models import OnecallWeather
from models import OnecallHourlyWeather
from models import OnecallDailyWeather
from models import CityList


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


def write_forecast(data):
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


def write_onecall(data):
    OnecallWeather(
        # Default name from DB column
        lon=data['lon'],
        lat=data['lat'],
        timezone=data['timezone'],
        # Current
        currentSunrise=data['current']['sunrise'],
        currentSunset=data['current']['sunset'],
        currentDateTime=data['current']['dt'],
        currentTemp=data['current']['temp'],
        currentFeelsLike=data['current']['feels_like'],
        currentPressure=data['current']['pressure'],
        currentHumidity=data['current']['humidity'],
        currentDewPoint=data['current']['dew_point'],
        currentUvi=data['current']['uvi'],
        currentClouds=data['current']['clouds'],
        currentVisibility=data['current']['visibility'],
        currentWindSpeed=data['current']['wind_speed'],
        currentWindDeg=data['current']['wind_deg'],
        currentWeatherId=data['current']['weather'][0]['id'],
        currentWeatherMain=data['current']['weather'][0]['main'],
        currentWeatherDescription=data['current']['weather'][0]['description'],
        currentWeatherIcon=data['current']['weather'][0]['icon'])
    for i in range(48):
        OnecallHourlyWeather(
            hourlyDateTime=data['hourly'][i]['dt'],
            hourlyTemp=data['hourly'][i]['temp'],
            hourlyFeelsLike=data['hourly'][i]['feels_like'],
            hourlyPressure=data['hourly'][i]['pressure'],
            hourlyHumidity=data['hourly'][i]['humidity'],
            hourlyDewPoint=data['hourly'][i]['dew_point'],
            hourlyClouds=data['hourly'][i]['cloudst'],
            hourlyWindSpeed=data['hourly'][i]['wind_speed'],
            hourlyWindDeg=data['hourly'][i]['wind_deg'],
            hourlyWeatherId=data['hourly'][i]['weather'][0]['id'],
            hourlyWeatherMain=data['hourly'][i]['weather'][0]['main'],
            hourlyWeatherDescription=data['hourly'][i]['weather'][0]['description'],
            hourlyWeatherIcon=data['hourly'][i]['weather'][0]['icon']
            )

    for j in range(8):
        OnecallDailyWeather(
            dailyDateTime=data['daily'][j]['dt'],
            dailySunrise=data['daily'][j]['sunrise'],
            dailySunset=data['daily'][j]['sunset'],
            dailyTempDay=data['daily'][j]['temp']['day'],
            dailyTempMin=data['daily'][j]['temp']['min'],
            dailyTempMax=data['daily'][j]['temp']['max'],
            dailyTempNight=data['daily'][j]['temp']['night'],
            dailyTempEvening=data['daily'][j]['temp']['eve'],
            dailyTempMorning=data['daily'][j]['temp']['morn'],
            dailyFeelsLikeDay=data['daily'][j]['feels_like']['day'],
            dailyFeelsLikeNight=data['daily'][j]['feels_like']['night'],
            dailyFeelsLikeEvening=data['daily'][j]['feels_like']['eve'],
            dailyFeelsLikeMorning=data['daily'][j]['feels_like']['morn'],
            dailyPressure=data['daily'][j]['pressure'],
            dailyHumidity=data['daily'][j]['humidity'],
            dailyDewPoint=data['daily'][j]['dew_point'],
            dailyWindSpeed=data['daily'][j]['wind_speed'],
            dailyWindDeg=data['daily'][j]['wind_deg'],
            dailyWeatherId=data['daily'][j]['weather'][0]['id'],
            dailyWeatherMain=data['daily'][j]['weather'][0]['main'],
            dailyWeatherDescription=data['daily'][j]['weather'][0]['description'],
            dailyWeatherIcon=data['daily'][j]['weather'][0]['icon'],
            dailyClouds=data['daily'][j]['clouds'],
            dailyRain=data['daily'][j]['rain'],
            dailyUvi=data['daily'][j]['uvi']
            )


def update_city_list(data):
    with open(data, 'r', encoding='utf-8') as json_file:
        city = json.load(json_file)
        for i in range(len(city)):
            CityList(cityId=city[i]['id'],
                     cityName=city[i]['name'],
                     state=city[i]['state'],
                     country=city[i]['country'],
                     lon=city[i]['coord']['lon'],
                     lat=city[i]['coord']['lat'])
    return


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Base

import sqlobject as orm


class Users(orm.SQLObject):
    """
        Table where we store user registration data.
    """
    userId = orm.IntCol(unique=True)
    userFirstName = orm.StringCol()
    userLastName = orm.StringCol()
    userName = orm.StringCol()
    languageCode = orm.StringCol()
    isBot = orm.BoolCol()
    #
    userTown = orm.String()
    userTownLon = orm.FloatCol()
    userTownLat = orm.FloatCol()


class CurrentWeather(orm.SQLObject):
    """
        Table where we store weather results at the time of
        user request
    """
    # Default name from DB column
    cityId = orm.IntCol()
    cityName = orm.StringCol()
    lon = orm.FloatCol()
    lat = orm.FloatCol()
    country = orm.StringCol()
    timezone = orm.IntCol()
    sunrise = orm.IntCol()
    sunset = orm.IntCol()
    dateTime = orm.IntCol()
    #
    weatherId = orm.IntCol()
    weatherMain = orm.StringCol()
    weatherDescription = orm.StringCol()
    weatherIcon = orm.StringCol()
    base = orm.StringCol()
    mainTemp = orm.FloatCol()
    mainFeelsLike = orm.FloatCol()
    mainTempMin = orm.FloatCol()
    mainTempMax = orm.FloatCol()
    mainPressure = orm.IntCol()
    mainHumidity = orm.IntCol()
    visibility = orm.IntCol()
    windSpeed = orm.FloatCol()
    windDeg = orm.IntCol()
    cloudsAll = orm.IntCol()
    sysType = orm.IntCol()
    sysId = orm.IntCol()


class ForecastWeather(orm.SQLObject):
    """
    """
    # Default name from DB column
    cityId = orm.IntCol()
    cityName = orm.StringCol()
    lon = orm.FloatCol()
    lat = orm.FloatCol()
    country = orm.StringCol()
    timezone = orm.IntCol()
    sunrise = orm.IntCol()
    sunset = orm.IntCol()
    dateTime = orm.IntCol()
    #
    dateTimeText = orm.StringCol()
    mainTemp = orm.FloatCol()
    mainFeelsLike = orm.FloatCol()
    mainTempMin = orm.FloatCol()
    mainTempMax = orm.FloatCol()
    mainPressure = orm.IntCol()
    mainSeaLevel = orm.IntCol()
    mainGroundLevel = orm.IntCol()
    mainHumidity = orm.IntCol()
    mainTempkf = orm.FloatCol()
    weatherId = orm.IntCol()
    weatherMain = orm.StringCol()
    weatherDescription = orm.StringCol()
    weatherIcon = orm.StringCol()
    cloudsAll = orm.IntCol()
    windSpeed = orm.FloatCol()
    windDeg = orm.IntCol()
    sysPod = orm.StringCol()


class OnecallWeather(orm.SQLObject):
    """
    """
    # Default name from DB column
    lon = orm.FloatCol()
    lat = orm.FloatCol()
    timezone = orm.StringCol()
    # Current
    currentSunrise = orm.IntCol()
    currentSunset = orm.IntCol()
    currentDateTime = orm.IntCol()
    currentTemp = orm.FloatCol()
    currentFeelsLike = orm.FloatCol()
    currentPressure = orm.IntCol()
    currentHumidity = orm.IntCol()
    currentDewPoint = orm.FloatCol()
    currentUvi = orm.FloatCol()
    currentClouds = orm.IntCol()
    currentVisibility = orm.IntCol()
    currentWindSpeed = orm.IntCol()
    currentWindDeg = orm.IntCol()
    currentWeatherId = orm.IntCol()
    currentWeatherMain = orm.StringCol()
    currentWeatherDescription = orm.StringCol()
    currentWeatherIcon = orm.StringCol()
    # Hourly
    hourlyDateTime = orm.IntCol()
    hourlyTemp = orm.FloatCol()
    hourlyFeelsLike = orm.FloatCol()
    hourlyPressure = orm.IntCol()
    hourlyHumidity = orm.IntCol()
    hourlyDewPoint = orm.FloatCol()
    hourlyClouds = orm.IntCol()
    hourlyWindSpeed = orm.IntCol()
    hourlyWindDeg = orm.IntCol()
    hourlyWeatherId = orm.IntCol()
    hourlyWeatherMain = orm.StringCol()
    hourlyWeatherDescription = orm.StringCol()
    hourlyWeatherIcon = orm.StringCol()
    # Daily
    dailyDateTime = orm.IntCol()
    dailySunrise = orm.IntCol()
    dailySunset = orm.IntCol()
    dailyTempDay = orm.FloatCol()
    dailyTempMin = orm.FloatCol()
    dailyTempMax = orm.FloatCol()
    dailyTempNight = orm.FloatCol()
    dailyTempEve = orm.FloatCol()
    dailyTempMorn = orm.FloatCol()
    dailyFeelsLikeDay = orm.FloatCol()
    dailyFeelsLikeNight = orm.FloatCol()
    dailyFeelsLikeEve = orm.FloatCol()
    dailyFeelsLikeMorn = orm.FloatCol()
    dailyPressure = orm.IntCol()
    dailyHumidity = orm.IntCol()
    dailyDewPoint = orm.FloatCol()
    dailyWindSpeed = orm.IntCol()
    dailyWindDeg = orm.IntCol()
    dailyWeatherId = orm.IntCol()
    dailyWeatherMain = orm.StringCol()
    dailyWeatherDescription = orm.StringCol()
    dailyWeatherIcon = orm.StringCol()
    dailyClouds = orm.IntCol()
    dailyUvi = orm.FloatCol()


class CityList(orm.SQLObject):
    """
        Table contents City list in Bulk JSON-file
    """
    cityId = orm.IntCol()
    cityName = orm.StringCol()
    state = orm.StringCol(default=None)
    country = orm.StringCol()
    lon = orm.FloatCol()
    lat = orm.FloatCol()


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

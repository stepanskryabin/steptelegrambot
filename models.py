#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Base

import sqlobject as orm


class Users(orm.SQLObject):
    """
        Create a table where we store user registration data.
    """
    userId = orm.IntCol(unique=True)
    userFirstname = orm.StringCol()
    userLastname = orm.StringCol()
    userName = orm.StringCol()
    languageCode = orm.StringCol()
    isBot = orm.BoolCol()


class CurrentWeather(orm.SQLObject):
    """
        Create a table where we store weather results at the time of
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
    pass


class CityList(orm.SQLObject):
    cityId = orm.IntCol()
    cityName = orm.StringCol()
    state = orm.StringCol(default=None)
    country = orm.StringCol()
    lon = orm.FloatCol()
    lat = orm.FloatCol()


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

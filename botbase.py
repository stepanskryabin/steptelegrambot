#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Create and work with database

import sqlobject as orm
import botconfig


connection = orm.connectionForURI(botconfig.OTHERSQL)
orm.sqlhub.processConnection = connection


class Users(orm.SQLObject):
    userId = orm.IntCol(unique=True)
    userFirstname = orm.StringCol()
    userLastname = orm.StringCol()
    userName = orm.StringCol()
    languageCode = orm.StringCol()
    isBot = orm.BoolCol()


class CurrentWeather(orm.SQLObject):
    cityId = orm.IntCol()
    cityName = orm.StringCol()
    lon = orm.FloatCol()
    lat = orm.FloatCol()
    dateTime = orm.IntCol()
    weatherId = orm.IntCol()
    weatherMain = orm.StringCol()
    weatherDescription = orm.StringCol()
    weatherIcon = orm.StringCol()
    base = orm.StringCol()
    mainTemp = orm.FloatCol()
    mainFeelsLike = orm.FloatCol()
    mainTempMin = orm.FloatCol()
    mainTempMax = orm.FloatCol()
    mainPressure = orm.FloatCol()
    mainHumidity = orm.FloatCol()
    visibility = orm.FloatCol()
    windSpeed = orm.FloatCol()
    cloudsAll = orm.IntCol()
    sysType = orm.IntCol()
    sysId = orm.IntCol()
    sysCountry = orm.StringCol()
    sysSunrise = orm.IntCol()
    sysSunset = orm.IntCol()
    timezone = orm.IntCol()


class DailyWeather(orm.SQLObject):
    pass


class HourlyWeather(orm.SQLObject):
    pass


class CityList(orm.SQLObject):
    cityId = orm.IntCol()
    cityName = orm.StringCol()
    state = orm.StringCol(default=None)
    country = orm.StringCol()
    lon = orm.FloatCol()
    lat = orm.FloatCol()


def city_database_fill():
    # with open('./lib/city.list.json', r)
    pass


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

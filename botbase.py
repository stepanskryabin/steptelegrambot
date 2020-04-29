#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Create and work with database

import sqlobject as orm
import botconfig

"""
    Choose the option to connect to the database, where:
    LOCAL_SQLITE: the bot_database.db file will be created
    in the local directory
    LOCAL_POSTGRESQL: a connection to a local server will be made
    ONLINE_POSTGRESQL: a connection will be made to a server hosted
    on the Internet.

    The settings are in the file botconfig.py.
"""
connection = orm.connectionForURI(botconfig.ONLINE_POSTGRESQL)
orm.sqlhub.processConnection = connection


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
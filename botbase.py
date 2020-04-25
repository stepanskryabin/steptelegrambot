#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Create and work with database

import sqlobject as orm
from os import path


base_path = path.abspath('bot_database.db')
database = 'sqlite:/:' + base_path
connection = orm.connectionForURI(database)
orm.sqlhub.processConnection = connection


class Users(orm.SQLObject):
    userId = orm.IntCol()
    isBot = orm.BoolCol()
    userFirstname = orm.StringCol()
    userLastname = orm.StringCol()
    useName = orm.StringCol()
    languageCode = orm.StringCol()


class CurrentWeather(orm.SQLObject):
    pass


class DailyWeather(orm.SQLObject):
    pass


class HourlyWeather(orm.SQLObject):
    pass


class CityList(orm.SQLObject):
    cityId = orm.IntCol()
    cityName = orm.UnicodeCol()
    country = orm.StringCol()
    coordLon = orm.FloatCol()
    coordLat = orm.FloatCol()


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

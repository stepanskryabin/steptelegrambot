#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Create and work with database

import sqlobject as orm
from os import path


base_path = path.abspath('bot_database.db')
database = 'sqlite:' + base_path
connection = orm.connectionForURI(database)
orm.sqlhub.processConnection = connection


class Users(orm.SQLObject):
    userId = orm.IntCol(unique=True)
    userFirstname = orm.StringCol()
    userLastname = orm.StringCol()
    userName = orm.StringCol()
    languageCode = orm.StringCol()
    isBot = orm.BoolCol()


class CurrentWeather(orm.SQLObject):
    pass


class DailyWeather(orm.SQLObject):
    pass


class HourlyWeather(orm.SQLObject):
    pass


class CityList(orm.SQLObject):
    pass


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

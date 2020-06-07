# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Models from database

import sqlobject as orm


class User(orm.SQLObject):
    """
        Table where we store user registration data.
    """
    userID = orm.IntCol(unique=True)
    userFirstName = orm.StringCol()
    userLastName = orm.StringCol()
    userName = orm.StringCol()
    languageCode = orm.StringCol()
    isBot = orm.BoolCol()
    userTown = orm.StringCol()
    userPassword = orm.StringCol()
    remindTime = orm.IntCol()
    remindDay = orm.IntCol()
    remindQuantity = orm.IntCol()


class AppConfig(orm.SQLObject):
    pass


class PaymenConfig(orm.SQLObject):
    pass


class AdminConfig(orm.SQLObject):
    pass


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

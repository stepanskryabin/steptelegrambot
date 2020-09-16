# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Models from database

import sqlobject as orm


class User(orm.SQLObject):
    """Creating a table of user settings in the database.

    Args:
        orm ([type]): [description]
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
    salt = orm.StringCol()


if __name__ == '__main__':
    print('This module does not need to be run as a separate process.')

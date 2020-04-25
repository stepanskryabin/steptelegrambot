#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Create and work with database

import sqlobject as orm
from os import path


class DataBase(orm.SQLObject):
    """
    Work with sqlite database via ORM SQLObject
    """

    def __init__(self):
        base_path = path.abspath('bot_database.db')
        self.database = 'sqlite:/:' + base_path
        self.connection = orm.connectionForURI(self.database)
        orm.sqlhub.processConnection = self.connection

    def create_users_table(self, name, *kwargs):
        pass

    def read_users_table(self, user_id):
        pass

    def read_collections_table(self, user_id):
        pass

    def write_users_table(self, values):
        pass

    def write_collections_table(self, values):
        pass

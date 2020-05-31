# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Manger
import sqlobject as orm
import time
import click

import botconfig
import models
from botbase import update_city_list

connection = orm.connectionForURI(botconfig.LOCAL_SQLITE)
orm.sqlhub.processConnection = connection


@click.command()
@click.option('--table', default='create', help='Create or delete all table \
    whit all data. The operation, by default, creates all tables')
def main(table):
    if table == "create":
        start_time = time.process_time()
        models.Users.createTable(ifNotExists=True)
        models.UsersSettings.createTable(ifNotExists=True)
        models.CurrentWeather.createTable(ifNotExists=True)
        models.ForecastWeather.createTable(ifNotExists=True)
        models.OnecallWeather.createTable(ifNotExists=True)
        models.CityList.createTable(ifNotExists=True)
        print(f"Table is createt at: {time.process_time() - start_time} sec.")
    elif table == "delete":
        start_time = time.process_time()
        models.Users.dropTable(
            ifExists=True, dropJoinTables=True, cascade=True)
        models.UsersSettings.dropTable(
            ifExists=True, dropJoinTables=True, cascade=True)
        models.CurrentWeather.dropTable(
            ifExists=True, dropJoinTables=True, cascade=True)
        models.ForecastWeather.dropTable(
            ifExists=True, dropJoinTables=True, cascade=True)
        models.OnecallWeather.dropTable(
            ifExists=True, dropJoinTables=True, cascade=True)
        models.CityList.dropTable(
            ifExists=True, dropJoinTables=True, cascade=True)
        print(f"Table is deleted at: {time.process_time() - start_time} sec.")
    elif table == 'update_city':
        start_time = time.process_time()
        update_city_list(botconfig.CITY_LIST)
        print(f'List of cities is loaded at: \
            {time.process_time() - start_time} sec.')
    else:
        return


if __name__ == "__main__":
    main()

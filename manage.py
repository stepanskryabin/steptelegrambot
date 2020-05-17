# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Manger
import sqlobject as orm
import botconfig
import click

import models

connection = orm.connectionForURI(botconfig.ONLINE_POSTGRESQL)
orm.sqlhub.processConnection = connection


@click.command()
@click.option('--table', default='create', help='Create or delete all table \
    whit all data. The operation, by default, creates all tables')
def main(table):
    if table == "create":
        models.Users.createTable(ifNotExists=True)
        models.UsersSettings.createTable(ifNotExists=True)
        models.CurrentWeather.createTable(ifNotExists=True)
        models.ForecastWeather.createTable(ifNotExists=True)
        models.OnecallWeather.createTable(ifNotExists=True)
        models.CityList.createTable(ifNotExists=True)
    elif table == "delete":
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
    else:
        return


@click.command()
@click.option('--city', help='download city list')
def fill_table(city):
    if city == 'update':
        pass
    elif city == 'delete':
        pass
    else:
        return


if __name__ == "__main__":
    main()

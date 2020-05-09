# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Manger
import sqlobject as orm
import botconfig
import click

import models

connection = orm.connectionForURI(botconfig.LOCAL_SQLITE)
orm.sqlhub.processConnection = connection


@click.command()
@click.option('--migrate', default='create_table', help='Create or delete all table \
    whit all data. The operation, by default, creates all tables')
def main(migrate):
    if migrate == "create_table":
        models.Users.createTable(ifNotExists=True)
        models.CurrentWeather.createTable(ifNotExists=True)
        models.ForecastWeather.createTable(ifNotExists=True)
        models.OnecallWeather.createTable(ifNotExists=True)
        models.CityList.createTable(ifNotExists=True)
    elif migrate == "delete_table":
        models.Users.dropTable()
        models.CurrentWeather.dropTable()
        models.ForecastWeather.dropTable()
        models.OnecallWeather.dropTable()
        models.CityList.dropTable()


if __name__ == "__main__":
    main()

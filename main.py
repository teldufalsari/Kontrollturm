import sqlite3
from os.path import exists

from Sources.bot import KontrollBot
from Sources.ConfigManager import ConfigManager

def databaseInit(path : str) -> None:
    try:
        # create DB
        sqlite_connection = sqlite3.connect(path)
        cursor = sqlite_connection.cursor()
        print('Database successfully created and connected')
        sqlite_select_query = 'select sqlite_version();'
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print('SQLite version: ', record)
        # create table in the DB
        sqlite_create_table_query = '''CREATE TABLE SU_WORKERS_DB (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT,
                                    data TEXT,
                                    type TEXT,
                                    text TEXT);'''
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print('Error while connecting to SQLite', error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print('Closed connection to SQLite')


def main():
    config = ConfigManager()
    if not exists(config.settings.database_file_path):
        databaseInit(config.settings.database_file_path)
    kt = KontrollBot(ConfigManager())
    kt.start()

if __name__ == '__main__':
    main()
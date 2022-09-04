import sqlite3

try:
    # creating DB
    sqlite_connection = sqlite3.connect('SU_WORKERS_DB.db')
    cursor = sqlite_connection.cursor()
    print("База данных создана и успешно подключена к SQLite")

    sqlite_select_query = "select sqlite_version();"
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
    print("Версия базы данных SQLite: ", record)
    
    # creating table in DB
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
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")
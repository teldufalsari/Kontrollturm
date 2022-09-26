import sqlite3
import logging
import time
import os.path
from datetime import datetime


def currentMilliTIme() -> int:
    return round(time.time() * 1000)


class DatabaseManager:
    database_path : os.path

    def __init__(self, database_path_ : os.path) -> None:
        self.database_path = database_path_


    def workStarted(self, name) -> None:
        sqlite_connection = None
        try:
            sqlite_connection = sqlite3.connect(self.database_path)
            cursor = sqlite_connection.cursor()
            sqlite_insert_with_param = '''INSERT OR IGNORE INTO workers_table
                                (id, name, data, type, text)
                                VALUES (?, ?, ?, ?, ?);'''
            now = datetime.now()
            print('user: [' + name + '] work started at ' + now.strftime('%d/%m/%Y %H:%M'))
            data_tuple = (currentMilliTIme(), name, now.strftime('%d/%m/%Y %H:%M'), 'startTime', '')
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqlite_connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            logging.critical('Error while inserting data into DB, caused by: ' + str(error))
            print(str(error))
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                logging.info('Inserted workStart to DB: [name = ' + name + ', time = ' + now.strftime('%d/%m/%Y %H:%M'))


    def workEnded(self, name, text) -> None:
        sqlite_connection = None
        try:
            sqlite_connection = sqlite3.connect(self.database_path)
            cursor = sqlite_connection.cursor()
            sqlite_insert_with_param = '''INSERT OR IGNORE INTO workers_table
                                (id, name, data, type, text)
                                VALUES (?, ?, ?, ?, ?);'''
            now = datetime.now()
            print('user: [' + name + '] work end at ' + now.strftime('%d/%m/%Y %H:%M') + ' with message + [' + text + ']')
            data_tuple = (currentMilliTIme(), name, now.strftime('%d/%m/%Y %H:%M'), 'endTime', text)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqlite_connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            logging.critical('Error while inserting data into DB, caused by: ' + str(error))
            print(str(error))
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                logging.info('Inserted workStart to DB: [name = ' + name + ', time = ' + now.strftime('%d/%m/%Y %H:%M'))


    def getEmployeeInfo(self, name) -> list:
        sqlite_connection = None
        result = []
        try:
            sqlite_connection = sqlite3.connect(self.database_path)
            cursor = sqlite_connection.cursor()
            sql_select_query = '''SELECT * 
                                  FROM workers_table
                                  WHERE name =''' + f"'{name}'"
            cursor.execute(sql_select_query)
            #lines = cursor.fetchall()
            #for line in lines:
            #    if line[1] == name:
            #        result.append(line)
            result = cursor.fetchall()
            cursor.close()
        except sqlite3.Error as error:
            logging.critical('Error while requesting data from DB, caused by: ' + str(error))
            print(str(error))
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                logging.info('Requested user from DB: [data = ' + str(result) + ']')
        if result != None and name != None:        
            print('user: [' + name + '] info: \n' + str(result))
        return result


    def getAll(self) -> list:
        sqlite_connection = None
        result = []
        try:
            sqlite_connection = sqlite3.connect(self.database_path)
            cursor = sqlite_connection.cursor()
            sql_select_query = '''SELECT * FROM workers_table'''
            cursor.execute(sql_select_query)
            lines = cursor.fetchall()
            result = lines
            cursor.close()
        except sqlite3.Error as error:
            logging.critical('Error while requesting data from DB, caused by: ' + str(error))
            print(str(error))
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                logging.info('Requested user from DB: [data = ' + str(result) + ']')
        return result

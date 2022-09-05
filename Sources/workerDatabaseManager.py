import sqlite3
import logging
from datetime import datetime
import config
import time

def current_milli_time():
    return round(time.time() * 1000)

def workStarted(name):
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect(config.database_path)
        cursor = sqlite_connection.cursor()

        sqlite_insert_with_param = """INSERT or IGNORE INTO SU_WORKERS_DB
                              (id, name, data, type, text)
                              VALUES (?, ?, ?, ?, ?);"""

        now = datetime.now()
        
        print("user: [" + name + "] work started at " + now.strftime("%d/%m/%Y %H:%M"))

        data_tuple = (current_milli_time(), name, now.strftime("%d/%m/%Y %H:%M"), "startTime", "")
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        logging.critical('Error while inserting data into DB, caused by: ' + str(error))
        print(str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            logging.info('Inserted workStart to DB: [name = ' + name + ', time = ' + now.strftime("%d/%m/%Y %H:%M"))
       
def workEnded(name, text):
    sqlite_connection = None
    
    try:
        sqlite_connection = sqlite3.connect(config.database_path)
        cursor = sqlite_connection.cursor()

        sqlite_insert_with_param = """INSERT or IGNORE INTO SU_WORKERS_DB
                              (id, name, data, type, text)
                              VALUES (?, ?, ?, ?, ?);"""

        now = datetime.now()
        
        print("user: [" + name + "] work end at " + now.strftime("%d/%m/%Y %H:%M") + " with message + [" + text + "]")

        data_tuple = (current_milli_time(), name, now.strftime("%d/%m/%Y %H:%M"), "endTime", text)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        logging.critical('Error while inserting data into DB, caused by: ' + str(error))
        print(str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            logging.info('Inserted workStart to DB: [name = ' + name + ', time = ' + now.strftime("%d/%m/%Y %H:%M"))

def getWorkerInfo(name):
    sqlite_connection = None
    result = []
    
    try:
        sqlite_connection = sqlite3.connect(config.database_path)
        cursor = sqlite_connection.cursor()

        sql_select_query = """select * from SU_WORKERS_DB"""
        cursor.execute(sql_select_query)
        
        lines = cursor.fetchall()
        
        for line in lines:
            if line[1] == name:
                result.append(line)
        
        cursor.close()

    except sqlite3.Error as error:
        logging.critical('Error while requesting data from DB, caused by: ' + str(error))
        print(str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            logging.info('Requested user from DB: [data = ' + str(result) + ']')
            
    if result != None:        
        print("user: [" + name + "] info: \n" + str(result))
            
    return result

def getAll():
    sqlite_connection = None
    result = []
    
    try:
        sqlite_connection = sqlite3.connect(config.database_path)
        cursor = sqlite_connection.cursor()

        sql_select_query = """select * from SU_WORKERS_DB"""
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
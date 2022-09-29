import sqlite3
import logging
import time
import os.path
from datetime import datetime
from unittest import result


def currentMilliTIme() -> int:
    return round(time.time() * 1000)

class DatabaseManager:
    database_path : os.path

    def __init__(self, database_path_ : os.path) -> None:
        self.database_path = database_path_

    def fetchLastRecordForUser(self, name : str) -> tuple:
        conn = None
        result = []
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            cur.execute(f'''
            SELECT * FROM workers_table
            WHERE name = '{name}' AND id = (
                SELECT MAX(id) FROM workers_table
                WHERE name = '{name}')
            ''')
            result = cur.fetchall()
            cur.close()
        except sqlite3.Error as error:
            logging.critical('Error while inserting data into DB, caused by: ' + str(error))
            print(str(error))
        finally:
            if conn:
                conn.close()
        if len(result) == 0:
            return None
        else:
            return result[0]

    def workStarted(self, name : str) -> None:
        conn = None
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            now = datetime.now()
            cur.execute(f'''
                INSERT OR IGNORE INTO workers_table
                (name, startDate, endDate, comments)
                VALUES ('{name}', '{now.strftime('%d.%m.%Y %H:%M')}', '', '')
            ''')
            print('user [' + name + '] started working at ' + now.strftime('%d.%m.%Y at %H:%M'))
            conn.commit()
            cur.close()
        except sqlite3.Error as error:
            logging.critical('Error while inserting data into DB, caused by: ' + str(error))
            print(str(error)) 
        finally:
            if conn:
                conn.close()
                logging.info('Started interval: [name = ' + name + ', time = ' + now.strftime('%d.%m.%Y %H:%M'))

    def workFinished(self, name : str, id : int, text : str) -> None:
        conn = None
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            now = datetime.now()
            cur.execute(f'''
                UPDATE workers_table
                SET endDate = '{now.strftime('%d.%m.%Y %H:%M')}', comments ='{text}'
                WHERE id={id}
            ''')
            print('user [' + name + '] finished working at ' + now.strftime('%d.%m.%Y at %H:%M'))
            conn.commit()
            cur.close()
        except sqlite3.Error as error:
            logging.critical('Error while inserting data into DB, caused by: ' + str(error))
            print(str(error))
        finally:
            if conn:
                conn.close()
                logging.info('Finished interval: [name = ' + name + ', time = ' + now.strftime('%d.%m.%Y %H:%M'))

    def fetchEmployeeInfo(self, name : str) -> list:
        conn = None
        result = []
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            cur.execute(f'''
                SELECT * FROM workers_table
                WHERE name = '{name}'
            ''')
            result = cur.fetchall()
            cur.close()
        except sqlite3.Error as error:
            logging.critical('Error while requesting data from DB, caused by: ' + str(error))
            print(str(error))
        finally:
            if conn:
                conn.close()
                logging.info('Requested user from DB: [data = ' + str(result) + ']')
        if result != None and name != None:        
            print(f'Info about [{name}] requested')
        return result

    def fetchAll(self) -> list:
        conn = None
        result = []
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            cur.execute('SELECT * FROM workers_table')
            result = cur.fetchall()
            cur.close()
        except sqlite3.Error as error:
            logging.critical('Error while requesting data from DB, caused by: ' + str(error))
            print(str(error))
        finally:
            if conn:
                conn.close()
                logging.info('All data from DB requested')
        return result

    def fetchDate(self, date : datetime) -> list:
        conn = None
        result = []
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            date_str = date.strftime('%d.%m.%Y') + '%'
            cur.execute(f'''
                SELECT * FROM workers_table
                WHERE startDate LIKE '{date_str}' OR endDate LIKE '{date_str}'
            ''')
            result = cur.fetchall()
            cur.close()
        except sqlite3.Error as error:
            logging.critical('Error while requesting data from DB, caused by: ' + str(error))
            print(str(error))
        finally:
            if conn:
                conn.close()
                logging.info(f'All data updated on [{date.strftime("%d.%m.%Y")}] requested')
        return result

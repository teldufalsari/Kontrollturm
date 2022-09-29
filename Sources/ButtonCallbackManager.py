from datetime import datetime
import io
import telebot

from Sources.ConfigManager import ConfigManager
from Sources.DatabaseManager import DatabaseManager


class ButtonCallbackManager:
    config : ConfigManager
    bot : telebot.TeleBot
    db_manager : DatabaseManager

    def __init__(self, config_ : ConfigManager, bot_ : telebot.TeleBot) -> None:
        self.config = config_
        self.bot = bot_
        self.db_manager = DatabaseManager(self.config.settings.database_file_path)

    def callMenu(self, chat):
        self.bot.send_message(chat.id, 'Menu', reply_markup=self.config.menu_builder.buildStartMenu(chat.username, self.config.privileged_users))

    def callDownloads(self, chat):
      self.bot.send_message(chat.id, 'Downloads', reply_markup=self.config.menu_builder.buildDownloadMenu())


    def dayComments(self, message, bot_dummy) -> None:
        interval = self.db_manager.fetchLastRecordForUser(message.chat.username)
        id = interval[0]
        self.db_manager.workFinished(message.chat.username, id, message.text)
        self.bot.send_message(message.chat.id, self.config.messages.finish_time_saved)
        self.callMenu(message.chat)


    def sendEmployeeInfo(self, message, bot_dummy) -> None:
        intervals = self.db_manager.fetchEmployeeInfo(message.text)
        if len(intervals) == 0:
            self.bot.send_message(message.chat.id, 'No records found')
            self.callMenu(message.chat)
            return
        last_interval = intervals[-1]
        start_count = len(intervals)
        if last_interval[3] == '':
            finish_count = start_count - 1
        else:
            finish_count = start_count
        msg = f'{self.config.messages.work_statistics} {message.text}:\n'
        msg += f'{self.config.messages.intervals_started}: {start_count}, {self.config.messages.intervals_finished}: {finish_count}\n'
        for i in range (0, finish_count):
            duration = datetime.strptime(intervals[i][3], '%d.%m.%Y %H:%M') - datetime.strptime(intervals[i][2], '%d.%m.%Y %H:%M')
            msg += f'-> {intervals[i][2]}, '
            msg += f'{self.config.messages.duration}: {duration}, {self.config.messages.tasks_completed}:\n{intervals[i][4]}\n'
        if finish_count != start_count:
            msg += f'-> {self.config.messages.unfinished_session}: {last_interval[2]}\n'
        self.bot.send_message(message.chat.id, msg)
        self.callMenu(message.chat)


    def workStartCallback(self, chat) -> None:
        last_interval = self.db_manager.fetchLastRecordForUser(chat.username)
        if last_interval == None:
            self.db_manager.workStarted(chat.username)
            self.bot.send_message(chat.id, self.config.messages.start_time_saved)
        else:
            if last_interval[3] == '':
                self.bot.send_message(chat.id, self.config.messages.interval_not_finished)
            else:
                self.db_manager.workStarted(chat.username)
                self.bot.send_message(chat.id, self.config.messages.start_time_saved)
        self.callMenu(chat)


    def workEndCallback(self, chat) -> None:
        last_interval = self.db_manager.fetchLastRecordForUser(chat.username)
        if last_interval == None:
            self.bot.send_message(chat.id, self.config.messages.interval_not_started)
            self.callMenu(chat)
            return
        if last_interval[3] != '':
            self.bot.send_message(chat.id, self.config.messages.interval_not_started)
            self.callMenu(chat)
        else:
            mesg = self.bot.send_message(chat.id, self.config.messages.write_report)
            self.bot.register_next_step_handler(mesg, self.dayComments, self.bot)


    def userInfoCallback(self, chat):
        mesg = self.bot.send_message(chat.id, self.config.messages.enter_employee_name + ':')
        self.bot.register_next_step_handler(mesg, self.sendEmployeeInfo, self.bot)


    def forTodayCallback(self, chat):
        intervals = self.db_manager.fetchDate(datetime.today())
        if len(intervals) == 0:
            self.bot.send_message(chat.id, 'Nothing to display')
            self.callMenu(chat)
            return
        users = {}
        for interval in intervals:
            if users.get(interval[1]) == None:
                users[interval[1]] = []
            users[interval[1]].append(interval)
        msg = ''
        for key, val in users.items():
            msg += f'{self.config.messages.employee_activity} {key}:\n'
            last_interval = val[-1]
            start_count = len(val)
            finish_count = (start_count - 1 if (last_interval[3] == '') else start_count)
            msg += f'{self.config.messages.intervals_started}: {start_count}, {self.config.messages.intervals_finished}: {finish_count}\n'
            for i in range(0, finish_count):
                duration = datetime.strptime(intervals[i][3], '%d.%m.%Y %H:%M') - datetime.strptime(intervals[i][2], '%d.%m.%Y %H:%M')
                msg += f'-> {self.config.messages.duration}: {duration}, {self.config.messages.tasks_completed}:\n{intervals[i][4]}\n'
            if start_count != finish_count:
                msg += f'-> {self.config.messages.unfinished_interval} since {last_interval[2]}\n'
        self.bot.send_message(chat.id, msg)
        self.callMenu(chat)


    def statusCallback(self, chat):
        intervals = self.db_manager.fetchEmployeeInfo(chat.username)
        if len(intervals) == 0:
            self.bot.send_message(chat.id, 'Nothing to display')
            self.callMenu(chat)
            return
        last_interval = intervals[-1]
        start_count = len(intervals)
        if (last_interval[3] == ''):
            finish_count = start_count - 1
        else:
            finish_count = start_count
        msg = self.config.messages.today_stats + ':\n'
        for i in range(0, finish_count):
            start_date = datetime.strptime(intervals[i][2], '%d.%m.%Y %H:%M')
            finish_date = datetime.strptime(intervals[i][3], '%d.%m.%Y %H:%M')
            if (start_date.date() == datetime.today().date()) or (finish_date.date() == datetime.today().date()):
                duration = finish_date - start_date
                msg += '->' + self.config.messages.duration + f': {duration}\n'
                msg += self.config.messages.tasks_completed + ':\n' + intervals[i][4] + '\n'
        if start_count != finish_count:
            msg += '->' + self.config.messages.unfinished_interval + ': ' + last_interval[2]
        self.bot.send_message(chat.id, msg)
        self.callMenu(chat)


    def downloadsCallback(self, chat):
        self.callDownloads(chat)


    def downloadUserCallback(self, chat):
        mesg = self.bot.send_message(chat.id, self.config.messages.enter_employee_name + ':')
        self.bot.register_next_step_handler(mesg, self.downloadUserInfo, self.bot)


    def downloadUserInfo(self, message, bot_dummy):
        intervals = self.db_manager.fetchEmployeeInfo(message.text)
        if len(intervals) == 0:
            self.bot.send_message(message.chat.id, self.config.messages.nothing_to_download)
            self.callMenu(message.chat)
            return
        tmp_file = self.config.messages.user_table_header + '\n'
        for interval in intervals:
            duration = datetime.strptime(interval[3], '%d.%m.%Y %H:%M') - datetime.strptime(interval[2], '%d.%m.%Y %H:%M')
            tmp_file += f'{interval[2]},{interval[3]},{duration},{interval[4]}\n'
        document = io.BytesIO(str.encode(tmp_file))
        document.name = message.text + '_stats.csv'
        self.bot.send_document(message.chat.id, document)
        self.callMenu(message.chat)


    def downloadDayCallback(self, chat):
        intervals = self.db_manager.fetchDate(datetime.today())
        if len(intervals) == 0:
            self.bot.send_message(chat.id, self.config.messages.nothing_to_download)
            self.callMenu(chat)
            return
        users = {}
        for interval in intervals:
            if users.get(interval[1]) == None:
                users[interval[1]] = []
            users[interval[1]].append(interval)
        tmp_file = self.config.messages.day_table_header + '\n'
        for key, val in users.items():
            last_interval = val[-1]
            start_count = len(val)
            finish_count = (start_count - 1 if (last_interval[3] == '') else start_count)
            for i in range(0, finish_count):
                duration = datetime.strptime(intervals[i][3], '%d.%m.%Y %H:%M') - datetime.strptime(intervals[i][2], '%d.%m.%Y %H:%M')
                tmp_file += f'{key},{duration},{intervals[i][4]}\n'
            if start_count != finish_count:
                tmp_file += f'{key}, {intervals[i][2]} - ...,<...>\n'
        document = io.BytesIO(str.encode(tmp_file))
        document.name = 'Today.csv'
        self.bot.send_document(chat.id, document)
        self.callMenu(chat)
            

    def downloadWholeDbCallback(self, chat):
        with open(self.config.settings.database_file_path, 'rb') as db_file:
            document = io.BytesIO(db_file.read())
            document.name = 'DB.s3db'
            self.bot.send_document(chat.id, document)
        self.callMenu(chat)

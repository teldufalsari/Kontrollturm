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


    def parseData(self, username):
        data = self.db_manager.getEmployeeInfo(username)
        starts = []
        ends = []
        descrs = []
        waiting_for = 'Start'
        for line in data:
            if line[3] == 'startTime':
                starts.append(datetime.strptime(line[2], '%d/%m/%Y %H:%M'))
                waiting_for = "end"
            if line[3] == 'endTime':
                ends.append(datetime.strptime(line[2], '%d/%m/%Y %H:%M'))
                descrs.append(line[4])
                waiting_for = 'start'
        return starts, ends, waiting_for, descrs


    def dayComments(self, message, bot_dummy) -> None:
        self.db_manager.workEnded(message.chat.username, message.text)
        self.bot.send_message(message.chat.id, self.config.messages.finish_time_saved)
        self.callMenu(message.chat)


    def nameAsk(self, message, bot_dummy) -> None:
        starts, ends, waiting_for, descrs = self.parseData(message.text)
        msg = self.config.messages.work_statistics + ' ' + message.text + ':\n'
        msg += self.config.messages.intervals_started + ': ' + str(len(starts)) + ', '
        msg += self.config.messages.intervals_finished + ': ' + str(len(ends)) + '\n'
        for i in range(min(len(starts), len(ends))):
            msg += '-> ' + str(starts[i].strftime('%d/%m/%Y'))
            msg += ', ' + self.config.messages.duration + str((ends[i]-starts[i])) + ', ' + self.config.messages.tasks_completed + ':\n' + descrs[i] + '\n'
        if len(starts) - 1 == len(ends):
            msg += '-> ' + self.config.messages.unfinished_session + ': ' + str(starts[-1].strftime('%d/%m/%Y %H:%M')) + '\n'
        self.bot.send_message(message.chat.id, msg)
        self.callMenu(message.chat)


    def workStartCallback(self, chat) -> None:
        starts, ends, waiting_for, descrs = self.parseData(chat.username)
        if len(starts) != len(ends):
            self.bot.send_message(chat.id, self.config.messages.interval_not_finished)
        else:
            self.db_manager.workStarted(chat.username)
            self.bot.send_message(chat.id, self.config.messages.start_time_saved)
        self.callMenu(chat)


    def workEndCallback(self, chat) -> None:
        starts, ends, waitingFor, descrs = self.parseData(chat.username)
        if len(starts) - 1 != len(ends):
            self.bot.send_message(chat.id, self.config.messages.interval_not_started)
            self.callMenu(chat)
        else:
            mesg = self.bot.send_message(chat.id, self.config.messages.write_report)
            self.bot.register_next_step_handler(mesg, self.dayComments, self.bot)


    def userInfoCallback(self, chat):
        mesg = self.bot.send_message(chat.id, self.config.messages.enter_employee_name + ':')
        self.bot.register_next_step_handler(mesg, self.nameAsk, self.bot)


    def forTodayCallback(self, chat):
        data = self.db_manager.getAll()
        users = {}
        for line in data:
            dt = datetime.fromtimestamp(int(line[0])/1000.0)
            if users.get(line[1]) == None:
                users[line[1]] = []
            if dt.date() == datetime.today().date():
                users[line[1]].append(line)

        for key, val in users.items():
            msg = self.config.messages.employee_activity + ' ' + key + '\n'
            starts = []
            ends = []
            descrs = []
            for line in val:
                if line[3] == 'startTime':
                    starts.append(datetime.strptime(line[2], '%d/%m/%Y %H:%M'))
                if line[3] == 'endTime':
                    ends.append(datetime.strptime(line[2], '%d/%m/%Y %H:%M'))
                    descrs.append(line[4])

            msg += self.config.messages.intervals_started + ': ' + str(len(starts)) + ', '
            msg += self.config.messages.intervals_finished + ': ' + str(len(ends)) + '\n'
            for i in range(min(len(starts), len(ends))):
                td = ends[i]-starts[i]
                msg += '-> ' + self.config.messages.duration +  str(td.seconds//3600) + ':' + str((td.seconds//60)%60) + ', '
                msg += self.config.messages.tasks_completed + ':\n' + descrs[i] + '\n'

            if len(starts) - 1 == len(ends):
                msg += '-> ' + self.config.messages.unfinished_session + ': ' + str(starts[-1].strftime('%H:%M')) + '\n'
            self.bot.send_message(chat.id, msg)
        self.callMenu(chat)


    def statusCallback(self, chat):
        data = self.db_manager.getAll()
        users = {}

        for line in data:
            dt = datetime.fromtimestamp(int(line[0])/1000.0)
            if users.get(line[1]) == None:
                users[line[1]] = []
            if dt.date() == datetime.today().date():
                users[line[1]].append(line)

        for key, val in users.items():
            if key != chat.username:
                continue
            msg = self.config.messages.today_stats + ':\n'
            starts = []
            ends = []
            descrs = []

            for line in val:
                if line[3] == 'startTime':
                    starts.append(datetime.strptime(line[2], '%d/%m/%Y %H:%M'))
                if line[3] == 'endTime':
                    ends.append(datetime.strptime(line[2], '%d/%m/%Y %H:%M'))
                    descrs.append(line[4])
            msg += self.config.messages.intervals_started + ': ' + str(len(starts)) + ', '
            msg += self.config.messages.intervals_finished + ': ' + str(len(ends)) + '\n'

            for i in range(min(len(starts), len(ends))):
                td = ends[i]-starts[i]
                msg += '-> ' + self.config.messages.duration + ': ' + str(td.seconds//3600) + ':' + str((td.seconds//60)%60) + ', '
                msg += self.config.messages.tasks_completed + ': \n' + descrs[i] + '\n'

            if len(starts) - 1 == len(ends):
                msg += '->' + self.config.messages.unfinished_interval + ': ' + str(starts[-1].strftime('%H:%M')) + '\n'
            self.bot.send_message(chat.id, msg)
        self.callMenu(chat)


    def downloadsCallback(self, chat):
        self.callDownloads(chat)


    def downloadUserCallback(self, chat):
        mesg = self.bot.send_message(chat.id, self.config.messages.enter_employee_name + ':')
        self.bot.register_next_step_handler(mesg, self.downloadUserInfo, self.bot)


    def downloadUserInfo(self, message, bot_dummy):
        starts, ends, waiting_for, descrs = self.parseData(message.text)
        tmp_file = ''
        for i in range(min(len(starts), len(ends))):
            tmp_file += str(starts[i].strftime('%d.%m.%Y')) + ','
            tmp_file += str(ends[i].strftime('%d.%m.%Y')) + ','
            tmp_file += str((ends[i]-starts[i])) + ','
            tmp_file += descrs[i] + '\n'
        if len(starts) - 1 == len(ends):
            tmp_file += str(starts[i].strftime('%d/%m/%Y')) + ',' 
            tmp_file += '-,' + '-,' + '-\n'
        
        if len(tmp_file) == 0:
            self.bot.send_message(message.chat.id, self.config.messages.nothing_to_download)
            self.callMenu(message.chat)
            return
        document = io.BytesIO(str.encode(tmp_file))
        document.name = message.text + '_stats.csv'
        self.bot.send_document(message.chat.id, document)
        self.callMenu(message.chat)


    def downloadDayCallback(self, chat):
        data = self.db_manager.getAll()
        users = {}
        for line in data:
            dt = datetime.fromtimestamp(int(line[0])/1000.0)
            if users.get(line[1]) == None:
                users[line[1]] = []
            if dt.date() == datetime.today().date():
                users[line[1]].append(line)

        for key, val in users.items():
            tmp_file = ''
            starts = []
            ends = []
            descrs = []
            for line in val:
                if line[3] == 'startTime':
                    starts.append(datetime.strptime(line[2], '%d.%m.%Y %H:%M'))
                if line[3] == 'endTime':
                    ends.append(datetime.strptime(line[2], '%d.%m.%Y %H:%M'))
                    descrs.append(line[4])
            for i in range(min(len(starts), len(ends))):
                duration = ends[i] - starts[i]
                tmp_file += key + ','
                tmp_file += str(duration.seconds//3600) + ':' + str((duration.seconds//60)%60) + ','
                tmp_file += descrs[i] + '\n'
            if len(starts) - 1 == len(ends):
                msg += '-> ' + self.config.messages.unfinished_session + ': ' + str(starts[-1].strftime('%H:%M')) + '\n'
                tmp_file += key + ',' + str(starts[-1].strftime('%H:%M')) + ' -,-\n'

            if len(tmp_file) == 0:
                self.bot.send_message(chat.id, self.config.messages.nothing_to_download)
                self.callMenu(chat)
                return

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

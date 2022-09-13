from datetime import datetime
import telebot
from telebot import types


import ConfigManager
import MenuBuilder
import workerDatabaseManager


class ButtonCallbackManager:
    config : ConfigManager.ConfigManager
    bot : telebot.TeleBot

    def __init__(self, config_, bot_ : ConfigManager.ConfigManager) -> None:
        self.config = config_
        self.bot = bot_

    def callMenu(self, chat):
        self.bot.send_message(chat.id, 'menu', reply_markup=MenuBuilder.buildStartMenu(chat.username))

    
    def parseData(self, username):
        data = workerDatabaseManager.getWorkerInfo(username)
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
    

    def dayComments(self, message) -> None:
        workerDatabaseManager.workEnded(message.chat.username, message.text)
        self.bot.send_message(message.chat.id, self.config.messages.finish_time_saved)
        self.bot.send_message(message.chat.id, 'menu', reply_markup=MenuBuilder.buildStartMenu(message.chat.username))


    def nameAsk(self, message) -> None:
        starts, ends, waiting_for, descrs = self.parseData()
        msg = self.config.messages.work_statistics + ' ' + message.text + '\n'
        msg += self.config.messages.intervals_started + ': ' + str(len(starts)) + ', '
        msg += self.config.messages.intervals_finished + ': ' + str(len(ends)) + '\n'
        for i in range(min(len(starts), len(ends))):
            msg += '-> ' + str(starts[i].strftime('%d/%m/%Y'))
            msg += ', ' + self.config.messages.duration + str((ends[i]-starts[i])) + ', ' + self.config.messages.tasks_completed + ':\n' + descrs[i] + '\n'
        if len(starts) - 1 == len(ends):
            msg += '-> ' + self.config.messages.unfinished_session + ': ' + str(starts[-1].strftime('%d/%m/%Y %H:%M')) + '\n'
        self.bot.send_message(message.chat.id, msg)
        self.bot.send_message(message.chat.id, 'menu', reply_markup=MenuBuilder.buildStartMenu(message.chat.username))


    def workStartCallback(self, chat) -> None:
        starts, ends, waiting_for, descrs = self.parseData(chat.username)
        if len(starts) != len(ends):
            self.bot.send_message(chat.id, self.config.messages.interval_not_finished)
        else:
            workerDatabaseManager.workStarted(chat.username)
            self.bot.send_message(chat.id, self.config.messages.start_time_saved)
        self.bot.send_message(chat.id, 'menu', reply_markup=MenuBuilder.buildStartMenu(chat.username))


    def workEndCallback(self, chat) -> None:
        starts, ends, waitingFor, descrs = self.parseData(chat.username)
        if len(starts) - 1 != len(ends):
            self.bot.send_message(chat.id, self.config.messages.interval_not_started)
            self.bot.send_message(chat.id, 'menu', reply_markup=MenuBuilder.buildStartMenu(chat.username))
        else:
            mesg = self.bot.send_message(chat.id, self.config.messages.write_report)
            self.bot.register_next_step_handler(mesg, self.DayComments, self.bot)


    def userInfoCallback(self, chat):
        mesg = self.bot.send_message(chat.id, self.config.messages.enter_employee_name)
        self.bot.register_next_step_handler(mesg, self.NameAsk, self.bot)


    def forTodayCallback(self, chat):
        data = workerDatabaseManager.getAll()
        users = {}
        for line in data:
            dt = datetime.fromtimestamp(int(line[0])/1000.0)
            if users.get(line[1]) == None:
                users[line[1]] = []
            if dt.date() == datetime.today().date():
                users[line[1]].append(line)
                
        for key, val in users.items():
            msg = self.config.messages.employee_activity + ' ' + key + "\n"
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
                msg += '-> ' + self.config.messages.unfinished_session + ': ' + str(starts[-1].strftime("%H:%M")) + '\n'
            self.bot.send_message(chat.id, msg)
        self.bot.send_message(chat.id, 'menu', reply_markup=MenuBuilder.buildStartMenu(chat.username))


    def statusCallback(self, chat):
        data = workerDatabaseManager.getAll()
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
                msg += '->' + self.config.messages.unfinished_interval + ': ' + str(starts[-1].strftime("%H:%M")) + '\n'
            self.bot.send_message(chat.id, msg)
        
        self.bot.send_message(chat.id, 'menu', reply_markup=MenuBuilder.buildStartMenu(chat.username))

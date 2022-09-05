import config
import menusBuilder
from datetime import datetime
from dateutil.relativedelta import relativedelta
from telebot import types
import workerDatabaseManager
import logging

def parseData(name):
    data = workerDatabaseManager.getWorkerInfo(name)

    starts = []
    ends = []
    descrs = []
    
    waitingFor = "start"
    
    for line in data:
        if line[3] == "startTime":
            starts.append(datetime.strptime(line[2], "%d/%m/%Y %H:%M"))
            waitingFor = "end"
        if line[3] == "endTime":
            ends.append(datetime.strptime(line[2], "%d/%m/%Y %H:%M"))
            descrs.append(line[4])
            waitingFor = "start"
            
    return starts, ends, waitingFor, descrs

def DayComments(message, bot):
    workerDatabaseManager.workEnded(message.chat.username, message.text)
    bot.send_message(message.chat.id, "Время окончания работы учтено...")
    bot.send_message(message.chat.id, "menu", reply_markup=menusBuilder.buildStartMenu(message.chat.username))

def NameAsk(message, bot):
    starts, ends, waitingFor, descrs = parseData(message.text)

    msg = "Информация о трудовых успехах товарища " + message.text + "\n"
    msg += "Отметок о начале: " + str(len(starts)) + ", отметок об окончании: " + str(len(ends)) + "\n"
    
    for i in range(min(len(starts), len(ends))):
        msg += "-> " + str(starts[i].strftime("%d/%m/%Y")) + ", длительность: " + str((ends[i]-starts[i])) + ", сделано: \n" + descrs[i] + "\n"
    
    if len(starts) - 1 == len(ends):
        msg += "-> Незаконченная сессия: " + str(starts[-1].strftime("%d/%m/%Y %H:%M")) + "\n"
    
    bot.send_message(message.chat.id, msg)
    bot.send_message(message.chat.id, "menu", reply_markup=menusBuilder.buildStartMenu(message.chat.username))

def WorkStartCallback(chat, bot):
    starts, ends, waitingFor, descrs = parseData(chat.username)
    
    if len(starts) != len(ends):
        bot.send_message(chat.id, "Вы не закончили предыдущий рабочий промежуток. Нажмите отметку об окончании.")
    else:
        workerDatabaseManager.workStarted(chat.username)
        bot.send_message(chat.id, "Время начала работы учтено...")
        
    bot.send_message(chat.id, "menu", reply_markup=menusBuilder.buildStartMenu(chat.username))

def WorkEndCallback(chat, bot):
    starts, ends, waitingFor, descrs = parseData(chat.username)
    
    if len(starts) - 1 != len(ends):
        bot.send_message(chat.id, "Вы не начали рабочую сессию. Нажмите отметку о начале.")
        bot.send_message(chat.id, "menu", reply_markup=menusBuilder.buildStartMenu(chat.username))
    else:
        mesg = bot.send_message(chat.id, "Напишите, что вы сделали за последний рабочий промежуток. Если вы ненадолго прерываете работу, то напишите причину.")
        bot.register_next_step_handler(mesg, DayComments, bot)
    
def UserInfoCallback(chat, bot):
    mesg = bot.send_message(chat.id, "Напишите имя товарища, успехи которого хотите узнать!")
    bot.register_next_step_handler(mesg, NameAsk, bot)
     
def ForTodayCallback(chat, bot):
    data = workerDatabaseManager.getAll()
    
    users = {}
    
    for line in data:
        dt = datetime.fromtimestamp(int(line[0])/1000.0)
        if users.get(line[1]) == None:
            users[line[1]] = []
        if dt.date() == datetime.today().date():
            users[line[1]].append(line)
            
    for key, val in users.items():
        msg = "Активность товарища " + key + "\n"
        starts = []
        ends = []
        descrs = []
        
        for line in val:
            if line[3] == "startTime":
                starts.append(datetime.strptime(line[2], "%d/%m/%Y %H:%M"))
            if line[3] == "endTime":
                ends.append(datetime.strptime(line[2], "%d/%m/%Y %H:%M"))
                descrs.append(line[4])
        
        msg += "Отметок о начале: " + str(len(starts)) + ", отметок об окончании: " + str(len(ends)) + "\n"
        
        for i in range(min(len(starts), len(ends))):
            td = ends[i]-starts[i]
            msg += "-> Длительность: " + str(td.seconds//3600) + ":" + str((td.seconds//60)%60) + ", сделано: \n" + descrs[i] + "\n"
    
        if len(starts) - 1 == len(ends):
            msg += "-> Незаконченная сессия: " + str(starts[-1].strftime("%H:%M")) + "\n"
        
        bot.send_message(chat.id, msg)
                
    bot.send_message(chat.id, "menu", reply_markup=menusBuilder.buildStartMenu(chat.username))
            
def StatusCallback(chat, bot):
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
    
        msg = "Статус текущего пользователя на сегодня:\n"
        starts = []
        ends = []
        descrs = []
        
        for line in val:
            if line[3] == "startTime":
                starts.append(datetime.strptime(line[2], "%d/%m/%Y %H:%M"))
            if line[3] == "endTime":
                ends.append(datetime.strptime(line[2], "%d/%m/%Y %H:%M"))
                descrs.append(line[4])
        
        msg += "Отметок о начале: " + str(len(starts)) + ", отметок об окончании: " + str(len(ends)) + "\n"
        
        for i in range(min(len(starts), len(ends))):
            td = ends[i]-starts[i]
            msg += "-> Длительность: " + str(td.seconds//3600) + ":" + str((td.seconds//60)%60) + ", сделано: \n" + descrs[i] + "\n"
    
        if len(starts) - 1 == len(ends):
            msg += "-> Незаконченный рабочий промежуток: " + str(starts[-1].strftime("%H:%M")) + "\n"
        
        bot.send_message(chat.id, msg)
                
    bot.send_message(chat.id, "menu", reply_markup=menusBuilder.buildStartMenu(chat.username))

import telebot
from telebot import types

def createMenuMarkup(buttons):
    markup = types.InlineKeyboardMarkup()
    for button in buttons:
        inline_button = types.InlineKeyboardButton(button[0], callback_data=button[1])
        markup.add(inline_button)
    return markup


def privilegedMenuMarkup():
    return createMenuMarkup([
        ['Отметка о начале работы', 'workStart'],
        ['Отметка о конце работы', 'workEnd'],
        ['Информация', 'userInfo'],
        ['Отчет за сегодня', 'forToday'],
        ['Статус', 'status']])


def unprivilegedMenuMarkup():
    return createMenuMarkup([
        ['Отметка о начале работы', 'workStart'],
        ['Отметка о конце работы', 'workEnd'],
        ['Статус', 'status']])    


def buildStartMenu(username):
    if username == "timattttt" or username == "arfarafar":
        return privilegedMenuMarkup()
    else:
        return unprivilegedMenuMarkup()

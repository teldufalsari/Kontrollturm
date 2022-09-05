from telebot import types

def buildMenu(buttons):
    markup = types.InlineKeyboardMarkup()
    
    for but in buttons:
        bb = types.InlineKeyboardButton(but[0], callback_data=but[1])
        markup.add(bb)
        
    return markup
        
def buildStartMenu(user):
    if user == "timattttt" or user == "arfarafar":
        return buildMenu([['Отметка о начале работы', 'WorkStart'],
                      ['Отметка о конце работы', 'WorkEnd'],
                      ['Информация', 'UserInfo'],
                      ['Отчет за сегодня', 'ForToday'],
                      ['Статус', 'Status']
               ])
    return buildMenu([['Отметка о начале работы', 'WorkStart'],
                      ['Отметка о конце работы', 'WorkEnd'],
                      ['Статус', 'Status']
               ])         
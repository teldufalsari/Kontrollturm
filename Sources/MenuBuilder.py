from telebot import types

from Sources.SettingsLists import ButtonsList

def createMenuMarkup(buttons) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    for button in buttons:
        inline_button = types.InlineKeyboardButton(button[0], callback_data=button[1])
        markup.add(inline_button)
    return markup


class MenuBuilder():
    buttons : ButtonsList

    def __init__(self, buttons_ : dict) -> None:
        self.buttons = buttons_

    def privilegedMenuMarkup(self) -> types.InlineKeyboardMarkup:
        return createMenuMarkup([
            [self.buttons.start_interval, 'workStart'],
            [self.buttons.finish_interval, 'workEnd'],
            [self.buttons.info, 'userInfo'],
            [self.buttons.today_report, 'forToday'],
            [self.buttons.status, 'status'],
            [self.buttons.downloads, 'downloads']])

    def unprivilegedMenuMarkup(self) -> types.InlineKeyboardMarkup:
        return createMenuMarkup([
            [self.buttons.start_interval, 'workStart'],
            [self.buttons.finish_interval, 'workEnd'],
            [self.buttons.status, 'status']])

    def buildStartMenu(self, username : str, privileged_users : dict) -> types.InlineKeyboardMarkup:
        if username in privileged_users:
            return self.privilegedMenuMarkup()
        else:
            return self.unprivilegedMenuMarkup()

    def buildDownloadMenu(self) -> types.InlineKeyboardMarkup:
        return createMenuMarkup([
            [self.buttons.download_user, 'downloadUser'],
            [self.buttons.download_day, 'downloadDay'],
            [self.buttons.download_whole_db, 'downloadWholeDb']])

import telebot
from telebot import types
import logging

import MenuBuilder
import ConfigManager
import ButtonCallbackManager

class KontrollBot:
    bot : telebot.TeleBot
    config : ConfigManager.ConfigManager
    callback_manager : ButtonCallbackManager.ButtonCallbackManager

    def __init__(self, config_ : ConfigManager.ConfigManager) -> None:
        self.config = config_
        logging.basicConfig(filename=self.config.settings.log_file_path, level=logging.DEBUG)
        self.bot = telebot.TeleBot(self.config.settings.token)
        self.callback_manager = ButtonCallbackManager.ButtonCallbackManager(self.config, self.bot)

        @self.bot.message_handler(commands=['start'])
        def starter(message):
            self.bot.send_message(message.chat.id, self.config.messages.prompt, reply_markup=MenuBuilder.buildStartMenu(message.chat.username))

        @self.bot.callback_query_handler(func=lambda call: True)
        def buttons(call):
            cbName = call.data
            getattr(self.callback_manager, cbName + 'Callback')(call.message.chat)
            self.bot.answer_callback_query(call.id)


    def start(self) -> None:
        logging.info('RouteVPN bot started...')
        self.bot.infinity_polling()

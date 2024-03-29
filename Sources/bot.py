import telebot
import logging

from Sources.MenuBuilder import MenuBuilder
from Sources.ConfigManager import ConfigManager
from Sources.ButtonCallbackManager import ButtonCallbackManager

class KontrollBot:
    bot : telebot.TeleBot
    config : ConfigManager
    callback_manager : ButtonCallbackManager

    def __init__(self, config_ : ConfigManager) -> None:
        self.config = config_
        logging.basicConfig(filename=self.config.settings.log_file_path, level=logging.DEBUG)
        self.bot = telebot.TeleBot(self.config.settings.token)
        self.callback_manager = ButtonCallbackManager(self.config, self.bot)

        @self.bot.message_handler(commands=['start'])
        def starter(message):
            self.bot.send_message(message.chat.id, self.config.messages.prompt, reply_markup=MenuBuilder.buildStartMenu(message.chat.username, self.config.privileged_users))

        @self.bot.callback_query_handler(func=lambda call: True)
        def buttons(call):
            cbName = call.data
            getattr(self.callback_manager, cbName + 'Callback')(call.message.chat)
            self.bot.answer_callback_query(call.id)


    def start(self) -> None:
        logging.info('RouteVPN bot started...')
        self.bot.infinity_polling()

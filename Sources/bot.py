import telebot
import logging

import buttonsCallbacks
import menusBuilder
import ConfigManager

def startBot(config : ConfigManager.ConfigManager) -> None:
    logging.basicConfig(filename=config.settings.log_file_path, level=logging.DEBUG)

    bot = telebot.TeleBot(config.token)

    @bot.message_handler(commands=['start'])
    def starter(message):
        bot.send_message(message.chat.id, config.messages.prompt, reply_markup=menusBuilder.buildStartMenu(message.chat.username))

    @bot.callback_query_handler(func=lambda call: True)
    def buttons(call):
        cbName = call.data
        getattr(buttonsCallbacks, cbName + 'Callback')(call.message.chat, bot)
        bot.answer_callback_query(call.id)

    logging.info('RouteVPN bot started...')

    bot.infinity_polling()


if __name__ == '__main__':
    startBot(ConfigManager.ConfigManager())

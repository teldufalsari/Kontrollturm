import config
import telebot
import menusBuilder
import logging
import buttonsCallbacks

logging.basicConfig(filename=config.log_file_name, level=logging.DEBUG)

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def starter(message):
    bot.send_message(message.chat.id, "Вас приветствует бот для сотрудников от компании SteelUnicorn LLC", reply_markup=menusBuilder.buildStartMenu(message.chat.username))

@bot.callback_query_handler(func=lambda call: True)
def buttons(call):
    cbName = call.data
    getattr(buttonsCallbacks, cbName + 'Callback')(call.message.chat, bot)
    bot.answer_callback_query(call.id)

logging.info('RouteVPN bot started...')

bot.infinity_polling()
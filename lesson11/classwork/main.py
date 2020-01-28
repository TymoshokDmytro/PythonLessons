from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from lesson11.classwork import config
from lesson11.classwork.keyboards import START_KB, NEWS_KB

bot = TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_bot(message):
    # print(message.text)
    # print(message.chat.id)
    # print(message.from_user.id)
    # pprint(message)
    #
    # bot.send_message(message.chat.id, "Hello")

    print(message)

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = [KeyboardButton(value) for value in START_KB.values()]
    kb.add(*buttons)

    bot.send_message(message.chat.id, 'Hello', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == START_KB['main'])
def main(message):
    bot.send_message(message.chat.id, 'Ты на главной странице')


@bot.message_handler(func=lambda message: message.text == START_KB['news'])
def get_news(message):
    kb = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(callback_data=key, text=txt) for key, txt in NEWS_KB.items()]
    kb.add(*buttons)
    bot.send_message(message.chat.id, 'Выберите новость', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    print(call)
    bot.send_message(call.message.chat.id, call.data)


# @bot.message_handler(content_types=['text'])
# def reversed(message):
#     text = message.text
#     bot.send_message(message.chat.id, 'Сам ты ' + text)
#
#
# @bot.message_handler(func=lambda message: message.text.lower() in WORDS.keys())
# def hello(message):
#     bot.send_message(message.chat.id, WORDS[message.text.lower()])
#
#
# @bot.message_handler(func=lambda message: message.text == 'Привет')
# def hello(message):
#     bot.send_message(message.chat.id, 'Привет')


if __name__ == "__main__":
    bot.polling()

from telebot import TeleBot

from .keyboards import START_KB
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from ..models.model import Category, Product, Texts

from .config import TOKEN

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    txt = Texts.objects.filter(text_type='Greetings').get()

    bot.send_message(message.chat.id, txt, reply_markup=ReplyKeyboardMarkup().add(
        *[KeyboardButton(button_name) for button_name in START_KB.values()]))

from mongoengine import DoesNotExist
from telebot import TeleBot
from re import match

from FinalProject.shop.bot.keyboards import START_KB, MAIN_KB
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove
from FinalProject.shop.models.model import Category, Product, Texts

from FinalProject.shop.bot.config import TOKEN
from lesson11.practice.bot.models.model import User, STATE

bot = TeleBot(token=TOKEN)


def check_registration(user, chat_id):
    if user.state != STATE.REGISTERED:
        text = ''
        if user.state == STATE.PHONE.name:
            text = 'Enter valid phone number (+380XXXXXXXXX):'
            user.state = STATE.PHONE_ENTERING.name
        elif user.state == STATE.EMAIL.name:
            text = 'Enter valid email (foo@foo.com):'
            user.state = STATE.EMAIL_ENTERING.name
        elif user.state == STATE.ADDRESS.name:
            text = 'Enter address:'
            user.state = STATE.ADDRESS_ENTERING_ENTERING.name
        if text:
            user.save()
            bot.send_message(chat_id, text)


def registration(user, value):
    if user.state != STATE.REGISTERED:
        state = None
        if user.state == STATE.PHONE.value:
            user.phone = value
            state = STATE.EMAIL.value
        elif user.state == STATE.EMAIL.value:
            user.email = value
            state = STATE.ADDRESS.value
        elif user.state == STATE.ADDRESS.value:
            user.email = value
            state = STATE.ADDRESS.value
        if state:
            user.state = state
            user.save()


def check_user_registered(message):
    try:
        user = User.objects.get(telegram_id=message.chat.id)
    except DoesNotExist:
        user = User.objects.create(telegram_id=message.chat.id,
                                   username=message.chat.first_name,
                                   fullname=message.chat.username)
    return user


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello ' + message.chat.username)
    user = check_user_registered(message.chat.id)
    if user.state != STATE.REGISTERED.value:
        bot.send_message(message.chat.id, 'You are not registered.')
        check_registration(user, chat_id=message.chat.id)


@bot.message_handler(content_types=['text'])
def text(message):
    user = check_user_registered(message.chat.id)
    if user.state != STATE.REGISTERED.name:
        registration(user, message.text)
        return


bot.polling()

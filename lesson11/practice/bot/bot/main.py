from datetime import datetime
from pprint import pprint

from mongoengine import DoesNotExist
from telebot import TeleBot
from re import match

from FinalProject.shop.config import TOKEN
from lesson11.practice.bot.models.model import User, STATE, Complient

bot = TeleBot(token=TOKEN)
phone_regex = '^\(?[\d]{3}\)?[\s-]?[\d]{3}[\s-]?[\d]{4}$'
email_regex = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""


def check_registration(user, chat_id):
    resp_text = ''
    if user.state == STATE.REGISTERED.value:
        resp_text = f'You are registered as:\nPhone: {user.phone}\nEmail: {user.email}\nAddress: {user.address}\nNow you can enter your complain:'
    else:
        if user.state == STATE.PHONE.value:
            resp_text = 'Enter valid phone number (ex (573)8841878 | 573-884-1234 | 573 234 1256):'
        elif user.state == STATE.EMAIL.value:
            resp_text = 'Enter valid email (foo@foo.com):'
        elif user.state == STATE.ADDRESS.value:
            resp_text = 'Enter address:'
    if resp_text:
        bot.send_message(chat_id, resp_text)


def registration(user, value):
    if user.state != STATE.REGISTERED:
        state = None
        text = ''
        if user.state == STATE.PHONE.value:
            if not match(phone_regex, value):
                return {'err': 'Not valid phone number. Try again'}
            user.phone = value
            state = STATE.EMAIL.value
        elif user.state == STATE.EMAIL.value:
            if not match(email_regex, value):
                return {'err': 'Not valid email number. Try again'}
            user.email = value
            state = STATE.ADDRESS.value
        elif user.state == STATE.ADDRESS.value:
            user.address = value
            state = STATE.REGISTERED.value
        if state:
            user.state = state
            user.save()

        return {}


def check_user_registered(message):
    try:
        user = User.objects.get(telegram_id=str(message.chat.id))
    except DoesNotExist:
        user = User.objects.create(telegram_id=str(message.chat.id),
                                   username=message.chat.first_name,
                                   fullname=message.chat.username)
    return user


@bot.message_handler(commands=['start', 'status', 'register'])
def start(message):
    bot.send_message(message.chat.id, 'Hello ' + message.chat.username)
    user = check_user_registered(message)
    if user.state != STATE.REGISTERED.value:
        bot.send_message(message.chat.id, 'You are not registered.')
    check_registration(user, chat_id=message.chat.id)


@bot.message_handler(commands=['show'])
def start(message):
    bot.send_message(message.chat.id, 'Hello ' + message.chat.username)
    user = check_user_registered(message)
    if user.state != STATE.REGISTERED.value:
        bot.send_message(message.chat.id, 'You are not registered. Type /register')
        return

    complaints = Complient.objects(user=user)

    pprint(list(complaints))

@bot.message_handler(content_types=['text'])
def text(message):
    user = check_user_registered(message)
    if user.state != STATE.REGISTERED.value:
        res = registration(user, message.text)
        if 'err' in res:
            bot.send_message(message.chat.id, res['err'])
        check_registration(user, chat_id=message.chat.id)
        return

    complient = Complient.objects.create(
        creation_date=datetime.now(),
        description=message.text,
        user=user
    )

    bot.send_message(message.chat.id, f'Your complient registered with id = {complient.id}')


bot.polling()

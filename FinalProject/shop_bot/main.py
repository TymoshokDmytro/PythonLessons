# -*- coding: utf-8 -*-
import datetime
import logging
import os
import threading

from flask import Flask, request, abort
from flask_restful import Api
from telebot import TeleBot
from telebot.types import Update

from api.resources import CategoryResource, ProductResource, UserResource
from config import TOKEN, PATH, WEBHOOK_URL
from keyboards import START_KB
from service.bot_service import BotService

app = Flask(__name__)
api = Api(app, prefix='/bot/v1')

api.add_resource(CategoryResource, '/category', '/category/<string:cat_id>')
api.add_resource(ProductResource, '/product', '/product/<string:product_id>')
api.add_resource(UserResource, '/user', '/user/<string:user_id>')

bot = TeleBot(TOKEN)
bs = BotService(bot)


def check_user(func):
    def wrapper(*args, **kwargs):
        telegram_id = args[0].from_user.id
        username = args[0].from_user.username
        BotService.check_user_by_telegram_id(telegram_id, username)
        return func(*args, **kwargs)

    return wrapper


@app.route(f'/{PATH}', methods=['POST'])
def webhook():
    """
    Function process webhook call
    """
    if request.headers.get('content-type') == 'application/json':

        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''

    else:
        abort(403)


@bot.inline_handler(func=lambda query: query.query.split('_')[0] == 'category')
@check_user
def inline_show_articles(query):
    categoty_title = query.query.split('_')[1]
    bs.show_articles_by_category_title(categoty_title, query.id)


@bot.inline_handler(func=lambda query: query.query == 'order_history')
@check_user
def order_history_inline(query):
    bs.order_history_inline(query)


@bot.inline_handler(func=lambda query: True)
@check_user
def inline(query):
    bs.process_inline(query)


@bot.message_handler(commands=['start'])
@check_user
def start(message):
    bs.start(message)


@bot.message_handler(func=lambda message: message.text == START_KB['categories'])
@check_user
def categories(message):
    bs.view_root_categories(message)


@bot.callback_query_handler(func=lambda call: call.data == 'total')
@check_user
def show_total(call):
    bs.show_total(call)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'product')
@check_user
def add_to_cart(call):
    bs.add_to_cart(call)


@bot.message_handler(func=lambda message: message.text == START_KB['cart'])
@check_user
def show_cart(message):
    bs.show_cart(message)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'cart')
@check_user
def cart_actions(call):
    bs.cart_actions(call)


@bot.callback_query_handler(func=lambda call: call.data == 'order')
@check_user
def order(call):
    bs.order(call)


@bot.message_handler(func=lambda message: message.text == START_KB['archive'])
@check_user
def categories(message):
    bs.show_archive(message)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'archive')
@check_user
def show_archive_cart(call):
    archived_cart_id = call.data.split('_')[1]
    bs.show_archive_cart(call, archived_cart_id)


@bot.callback_query_handler(func=lambda call: call.data == 'personal_info')
@check_user
def personal_info(call):
    bs.personal_info(call)


@bot.callback_query_handler(func=lambda call: True)
@check_user
def get_cat_or_products(call):
    if call.data == START_KB['categories']:
        return bs.view_root_categories(call.message)
    bs.show_categories(call.data, message=call.message)


@bot.message_handler(func=lambda message: message.text == START_KB['promo'])
@check_user
def show_promo_products(message):
    bs.show_promo_products(message)


@bot.message_handler(func=lambda message: message.text == START_KB['personal'])
@check_user
def personal(message):
    bs.personal(message)


if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(filename='logs/log_' + datetime.date.today().strftime("%Y_%m_%d") + '_bot.log',
                        datefmt="%Y_%m_%d %H:%M:%S",
                        level=logging.DEBUG)

    # if need to seed the database, just use:
    # ShopDataGenerator.generate_data()
    bot.polling()
    # import time
    #
    # print('Started TELEGRAM BOT SHOP WEB SERVER')
    # bot.remove_webhook()
    # time.sleep(3)
    # bot.set_webhook(
    #     url=WEBHOOK_URL,
    #     certificate=open('nginx-selfsigned.crt', 'r')
    # )
    # app.run(host='127.0.0.1', port=5000)

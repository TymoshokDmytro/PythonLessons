# -*- coding: utf-8 -*-
from pprint import pprint

from flask import Flask, request, abort
from telebot import TeleBot
from telebot.types import Update, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, \
    InputTextMessageContent

from config import TOKEN, PATH
from keyboards import START_KB
from models.model import Product
from models.seader import ShopDataGenerator
from service.bot_service import BotService

app = Flask(__name__)

bot = TeleBot(TOKEN)
bs = BotService(bot)


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


@bot.inline_handler(func=lambda query: True)
def inline(query):
    data = query.query
    if not data:
        return

    query_set = Product.objects(title__contains=data)
    if query_set.count() == 0:
        return
    results = []
    for i, product in enumerate(product for product in query_set):
        kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text='В корзину', callback_data='product_' + str(product.id))
        kb.add(button)

        temp_res = InlineQueryResultArticle(
            id=i + 1,
            title=product.title,
            description=product.description,
            # input_message_content=InputTextMessageContent(message_text='Текст после нажатия на инайн кнопку',                                                                ),
            # input_message_content=types.InputMediaPhoto(
            #     media='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTn8DQPz__lgLXqLR__jYIqOqt-4g4AC56kcc2hrbSUva4Ucnvo',
            #     caption='Описание'
            # ),
            input_message_content=InputTextMessageContent(
                parse_mode='HTML',
                disable_web_page_preview=False,
                message_text=bs.get_product_desc_for_message(product)
            ),
            thumb_url=product.img_url if product.img_url else '',
            reply_markup=kb

        )
        results.append(temp_res)

    bot.answer_inline_query(query.id, results, cache_time=0)


@bot.message_handler(commands=['start'])
def start(message):
    bs.start(message)


@bot.message_handler(func=lambda message: message.text == START_KB['categories'])
def categories(message):
    bs.view_root_categories(message)


@bot.callback_query_handler(func=lambda call: call.data == 'total')
def show_total(call):
    bs.show_total(call)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'product')
def add_to_cart(call):
    bs.add_to_cart(call)


@bot.message_handler(func=lambda message: message.text == START_KB['cart'])
def show_cart(message):
    bs.show_cart(message)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'cart')
def cart_actions(call):
    bs.cart_actions(call)


@bot.callback_query_handler(func=lambda call: True)
def get_cat_or_products(call):
    if call.data == START_KB['categories']:
        return bs.view_root_categories(call.message)
    bs.show_categories(call.data, message=call.message)


@bot.message_handler(func=lambda message: message.text == START_KB['promo'])
def show_promo_products(message):
    bs.show_promo_products(message)


if __name__ == '__main__':
    # if need to seed the database, just use:
    # ShopDataGenerator.generate_data()
    bot.polling()

#     import time
#
#     print('Started TELEGRAM BOT SHOP WEB SERVER')
#     bot.remove_webhook()
#     time.sleep(1)
#     bot.set_webhook(
#         url=WEBHOOK_URL,
#         certificate=open('nginx-selfsigned.crt', 'r')
#     )
#     app.run(host='127.0.0.1', port=5000, debug=True)

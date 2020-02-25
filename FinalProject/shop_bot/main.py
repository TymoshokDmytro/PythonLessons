# -*- coding: utf-8 -*-
import json
from pprint import pprint

from flask import Flask, request, abort
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update

from config import TOKEN, PATH
from keyboards import START_KB
from models.model import Category, Product, Cart, CartProduct

bot = TeleBot(token=TOKEN)

app = Flask(__name__)


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


@bot.message_handler(commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup()
    buttons = [KeyboardButton(button_name) for button_name in START_KB.values()]
    kb.add(*buttons)
    bot.send_message(message.chat.id, 'Welcome to online store, ' + str(message.from_user.username), reply_markup=kb)


def view_root_categories(message):
    cats = Category.objects(is_root=True)

    kb = InlineKeyboardMarkup()

    buttons = [InlineKeyboardButton(text=cat.title, callback_data=str(cat.id)) for cat in cats]

    kb.add(*buttons)
    txt = 'Выберите категорию'
    if message.from_user.is_bot:
        return bot.edit_message_text(txt,
                                     message_id=message.message_id,
                                     chat_id=message.chat.id,
                                     reply_markup=kb)

    bot.send_message(message.chat.id, txt, reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == START_KB['categories'])
def categories(message):
    view_root_categories(message)


@bot.callback_query_handler(func=lambda call: call.data == 'total')
def show_total(call):
    user_id = str(call.message.chat.id)
    user_cart = Cart.objects(user=user_id)
    if not user_cart:
        bot.send_message(call.message.chat.id, 'No products in cart yet')
    else:
        user_cart = user_cart.first()

    reply_markup = call.message.json['reply_markup']
    text = reply_markup['inline_keyboard'][0][0]['text']
    reply_markup['inline_keyboard'][0][0]['text'] = f'TOTAL: {user_cart.get_total_str()}'
    if text == reply_markup['inline_keyboard'][0][0]['text']:
        return
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=json.dumps(reply_markup))


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'product')
def add_to_cart(call):
    product = Product.objects.get(id=call.data.split('_')[1])

    user_id = str(call.message.chat.id)
    user_cart = Cart.objects(user=user_id)
    if not user_cart:
        user_cart = Cart.objects.create(user=user_id)
    else:
        user_cart = user_cart.first()

    user_cart.add_product_to_cart(product)
    bot.send_message(call.message.chat.id, f'Product {product.title} added to cart')


@bot.message_handler(func=lambda message: message.text == START_KB['cart'])
def show_cart(message):
    user_id = str(message.chat.id)
    user_cart = Cart.objects(user=user_id)
    if not user_cart or user_cart.first().get_size() == 0:
        return bot.send_message(user_id, 'No articles yet in cart')

    user_cart = user_cart.first()
    frequencies = user_cart.get_cart().item_frequencies('product')

    products_dict = {cart_product.product.id: cart_product for cart_product in user_cart.get_cart()}
    pprint(products_dict)
    print()
    # ✔️ 2714
    for key, cart_product in products_dict.items():
        qty = frequencies[key]
        cart_prod_text = f'{cart_product.product.title}\n' \
                         f'Price: {cart_product.product.get_price_str()}\n' \
                         f'Total: {cart_product.product.get_total_str(qty)}\n'

        kb = InlineKeyboardMarkup()
        buttons = [
            InlineKeyboardButton(text=u'\U00002796', callback_data='cart_decrease_' + str(key)),
            InlineKeyboardButton(text=str(qty), callback_data='cart_nothing'),
            InlineKeyboardButton(text=u'\U00002795', callback_data='cart_increase_' + str(key)),
            InlineKeyboardButton(text=u'\U0000274C', callback_data='cart_remove_' + str(key))
        ]
        kb.add(*buttons)  # 2795
        bot.send_message(user_id, cart_prod_text, reply_markup=kb)

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='TOTAL', callback_data='total'))
    kb.add(
        InlineKeyboardButton(text='ORDER ' + u'\U00002714', callback_data='order'),
        InlineKeyboardButton(text='REMOVE ALL  ' + u'\U0000274C', callback_data='cart_drop'),
    )

    bot.send_message(user_id, 'Order:', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'cart')
def cart_actions(call):
    action = call.data.split('_')[1]

    if action == 'nothing':
        return

    user_id = str(call.message.chat.id)
    cart = Cart.objects(user=user_id).first()

    if action == 'drop':
        cart.remove_all_from_cart()
        return bot.send_message(user_id, 'All products removed from cart')

    product_id = str(call.data.split('_')[2])
    product = Product.objects(id=product_id).get()

    if action == 'remove':
        cart.remove_product_from_cart(product)
        bot.delete_message(user_id, message_id=call.message.message_id)
        return

    reply_markup = call.message.json['reply_markup']
    rp_t = reply_markup['inline_keyboard'][0][1]['text']

    if action == 'increase':
        cart.add_product_to_cart(product)
        rp_t = str(int(rp_t) + 1)

    if action == 'decrease':
        if cart.get_product_qty(product) == 0:
            return
        cart.delete_product_from_cart(product)
        rp_t = str(int(rp_t) - 1)
        if rp_t == '0':
            bot.delete_message(user_id, message_id=call.message.message_id)
            return
    reply_markup['inline_keyboard'][0][1]['text'] = rp_t
    cart_prod_text = f'{product.title}\n' \
                     f'Price: {product.get_price_str()}\n' \
                     f'Total: {product.get_total_str(int(rp_t))}\n'

    bot.edit_message_text(text=cart_prod_text, chat_id=user_id, message_id=call.message.message_id,
                          reply_markup=json.dumps(reply_markup))


@bot.callback_query_handler(func=lambda call: True)
def get_cat_or_products(call):
    """
    Приходит к нам id категории, получаем объект этой категории:
    1) Если объект не имеет предков - выводим продукты
    2) Если объект имеет предков - выводит этих предков

    :param call:
    :return:
    """
    if call.data == START_KB['categories']:
        return view_root_categories(call.message)

    show_categories(call.data, message=call.message)


def show_categories(data, message):
    kb = InlineKeyboardMarkup()
    title_text = ' | Категории:'
    category = Category.objects.get(id=data)
    buttons = []

    if category.subcategories:
        buttons = [InlineKeyboardButton(text=cat.title, callback_data=str(cat.id)) for cat in category.subcategories]

    if not category.is_root:
        buttons.append(InlineKeyboardButton(text='<<< Назад', callback_data=str(category.parent.id)))
    buttons.append(InlineKeyboardButton(text='^ В начало', callback_data=START_KB['categories']))
    kb.add(*buttons)

    if not category.subcategories:
        title_text = ' | Товары:'
        for product in category.get_products():
            kb_pr = InlineKeyboardMarkup()
            kb_pr.add(InlineKeyboardButton(text='В корзину', callback_data='product_' + str(product.id)))
            caption = 'TITLE:' + product.title + '\nDESC: ' + product.description + '\nPRICE: ' + product.get_price_markdown_str()
            bot.send_message(message.chat.id,
                             # caption + ('<a href="' + product.img_url + '">&#8205;</a>' if product.img_url else ''),
                             caption + ("<a href='" + product.img_url + "'>&#8205</a>" if product.img_url else ''),
                             parse_mode='HTML',
                             reply_markup=kb_pr)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, category.title + title_text, reply_markup=kb)
        return

    bot.edit_message_text(category.title + title_text,
                          message_id=message.message_id,
                          chat_id=message.chat.id,
                          reply_markup=kb)


if __name__ == '__main__':
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

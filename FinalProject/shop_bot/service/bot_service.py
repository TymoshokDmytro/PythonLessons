import json
import time

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from keyboards import START_KB
from models.model import Category, Product, Cart


class BotService:

    def __init__(self, bot_instanse):
        self._bot = bot_instanse

    def view_root_categories(self, message):
        cats = Category.objects(is_root=True)
        kb = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton(text=cat.title, callback_data=str(cat.id)) for cat in cats]
        kb.add(*buttons)
        if message.from_user.is_bot:
            return self._bot.edit_message_text('Выберите категорию',
                                               message_id=message.message_id,
                                               chat_id=message.chat.id,
                                               reply_markup=kb)

        self._bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=kb)

    def show_categories(self, data, message):
        kb = InlineKeyboardMarkup()
        title_text = ' | Категории:'
        category = Category.objects.get(id=data)
        buttons = []

        if category.subcategories:
            buttons = [InlineKeyboardButton(text=cat.title, callback_data=str(cat.id)) for cat in
                       category.subcategories]

        if not category.is_root:
            buttons.append(InlineKeyboardButton(text='<<< Назад', callback_data=str(category.parent.id)))
        buttons.append(InlineKeyboardButton(text='^ В начало', callback_data=START_KB['categories']))
        kb.add(*buttons)

        if not category.subcategories:
            title_text = ' | Товары:'
            self.show_products(category.get_products(), message.chat.id)
            self._bot.delete_message(message.chat.id, message.message_id)
            self._bot.send_message(message.chat.id, category.title + title_text, reply_markup=kb)
            return

        self._bot.edit_message_text(category.title + title_text,
                                    message_id=message.message_id,
                                    chat_id=message.chat.id,
                                    reply_markup=kb)

    @staticmethod
    def get_product_desc_for_message(product):
        return f"""
<b>TITLE</b>: {product.title} 
<b>DESC</b>: {product.description} 
<b>PRICE</b>:  {product.get_price_markdown_str()}
<b>IN_STOCK</b>: {product.in_stock}
{"<a href='" + product.img_url + "'>&#8205</a>" if product.img_url else ''}
        """

    def show_products(self, products, chat_id):
        for product in products:
            kb_pr = InlineKeyboardMarkup()
            kb_pr.add(InlineKeyboardButton(text='В корзину', callback_data='product_' + str(product.id)))
            self._bot.send_message(chat_id,
                                   self.get_product_desc_for_message(product),
                                   parse_mode='HTML',
                                   # disable_web_page_preview=True,
                                   reply_markup=kb_pr)

    def cart_actions(self, call):
        action = call.data.split('_')[1]

        if action == 'nothing':
            return

        user_id = str(call.message.chat.id)
        cart = Cart.objects(user=user_id).first()

        if action == 'drop':
            cart.remove_all_from_cart()
            return self._bot.send_message(user_id, 'All products removed from cart')

        product_id = str(call.data.split('_')[2])
        product = Product.objects(id=product_id).get()

        if action == 'remove':
            cart.remove_product_from_cart(product)
            self._bot.delete_message(user_id, message_id=call.message.message_id)
            return

        reply_markup = call.message.json['reply_markup']
        rp_t = reply_markup['inline_keyboard'][0][1]['text']

        if action == 'increase':
            if product.in_stock == int(rp_t):
                self._bot.edit_message_text(text=call.message.text + f"\n<b>MAX STOCK ITEMS REACHED</b>",
                                            parse_mode='HTML',
                                            chat_id=user_id,
                                            message_id=call.message.message_id,
                                            reply_markup=json.dumps(reply_markup))
                time.sleep(2)
                self._bot.edit_message_text(text=call.message.text,
                                            chat_id=user_id,
                                            message_id=call.message.message_id,
                                            reply_markup=json.dumps(reply_markup))
                return
            cart.add_product_to_cart(product)
            rp_t = str(int(rp_t) + 1)

        if action == 'decrease':
            if cart.get_product_qty(product) == 0:
                return
            cart.delete_product_from_cart(product)
            rp_t = str(int(rp_t) - 1)
            if rp_t == '0':
                self._bot.delete_message(user_id, message_id=call.message.message_id)
                return
        reply_markup['inline_keyboard'][0][1]['text'] = rp_t
        cart_prod_text = f'{product.title}\n' \
                         f'Price: {product.get_price_str()}\n' \
                         f'Total: {product.get_total_str(int(rp_t))}\n'

        self._bot.edit_message_text(text=cart_prod_text, chat_id=user_id, message_id=call.message.message_id,
                                    reply_markup=json.dumps(reply_markup))

    def show_cart(self, message):
        user_id = str(message.chat.id)
        user_cart = Cart.objects(user=user_id)
        if not user_cart or user_cart.first().get_size() == 0:
            return self._bot.send_message(user_id, 'No articles yet in cart')

        user_cart = user_cart.first()
        frequencies = user_cart.get_cart().item_frequencies('product')

        products_dict = {cart_product.product.id: cart_product for cart_product in user_cart.get_cart()}
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
            self._bot.send_message(user_id, cart_prod_text, reply_markup=kb)

        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton(text='TOTAL', callback_data='total'))
        kb.add(
            InlineKeyboardButton(text='ORDER ' + u'\U00002714', callback_data='order'),
            InlineKeyboardButton(text='REMOVE ALL  ' + u'\U0000274C', callback_data='cart_drop'),
        )

        self._bot.send_message(user_id, 'Order:', reply_markup=kb)

    def add_to_cart(self, call):
        user_id = str(call.from_user.id)
        product = Product.objects.get(id=call.data.split('_')[1])
        # if stock = 0 we cannot add this prod to cart
        if product.in_stock == 0:
            return self._bot.send_message(user_id, f'Cannot add product {product.title} because it is out of stock')

        user_cart = Cart.objects(user=user_id)
        if not user_cart:
            user_cart = Cart.objects.create(user=user_id)
        else:
            user_cart = user_cart.first()

        user_cart.add_product_to_cart(product)
        self._bot.send_message(user_id, f'Product {product.title} added to cart')

    def show_total(self, call):
        user_id = str(call.message.chat.id)
        user_cart = Cart.objects(user=user_id)
        if not user_cart:
            self._bot.send_message(call.message.chat.id, 'No products in cart yet')
        else:
            user_cart = user_cart.first()

        reply_markup = call.message.json['reply_markup']
        text = reply_markup['inline_keyboard'][0][0]['text']
        reply_markup['inline_keyboard'][0][0]['text'] = f'TOTAL: {user_cart.get_total_str()}'
        if text == reply_markup['inline_keyboard'][0][0]['text']:
            return
        self._bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                            reply_markup=json.dumps(reply_markup))

    def start(self, message):
        kb = ReplyKeyboardMarkup()
        buttons = [KeyboardButton(button_name) for button_name in START_KB.values()]
        kb.add(*buttons)
        self._bot.send_message(message.chat.id, 'Welcome to online store, ' + str(message.from_user.username),
                               reply_markup=kb)

    def show_promo_products(self, message):
        self._bot.delete_message(message.chat.id, message.message_id)
        promo_products_query = Product.objects.filter(discount_price__exists=True)
        if promo_products_query.count() == 0:
            return self._bot.send_message(message.chat.id, 'No discount products found')
        promo_products = []
        [promo_products.append(promo_product) for promo_product in promo_products_query]
        self.show_products(promo_products, message.chat.id)

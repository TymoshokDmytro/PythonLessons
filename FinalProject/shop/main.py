from telebot import TeleBot

from FinalProject.shop.keyboards import START_KB
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from FinalProject.shop.models.model import Category

from FinalProject.shop.config import TOKEN

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    # txt = Texts.objects(text_type='Greetings').get()
    txt = 'hello'

    kb = ReplyKeyboardMarkup()
    buttons = [KeyboardButton(button_name) for button_name in START_KB.values()]
    kb.add(*buttons)
    bot.send_message(message.chat.id, txt, reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == START_KB['categories'])
def categories(message):
    cats = Category.objects(is_root=True)

    kb = InlineKeyboardMarkup()

    buttons = [InlineKeyboardButton(text=cat.title, callback_data=str(cat.id)) for cat in cats]

    kb.add(*buttons)
    bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def get_cat_or_products(call):
    """
    Приходит к нам id категории, получаем объект этой категории:
    1) Если объект не имеет предков - выводим продукты
    2) Если объект имеет предков - выводит этих предков

    :param call:
    :return:
    """
    kb = InlineKeyboardMarkup()
    title_text = ' | Категории:'
    category = Category.objects.get(id=call.data)
    buttons = []

    if category.subcategories:
        buttons = [InlineKeyboardButton(text=cat.title, callback_data=str(cat.id)) for cat in category.subcategories]

    else:
        title_text = ' | Товары:'
        buttons = [
            InlineKeyboardButton(text=product.title, callback_data=str(product.id)) for product in
            category.get_products()
        ]

    kb.add(*buttons)
    bot.edit_message_text(category.title + title_text,
                          message_id=call.message.message_id,
                          chat_id=call.message.chat.id,
                          reply_markup=kb)
    # bot.send_message(call.message.chat.id, category.title, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'product')
def add_to_cart(call):
    product = call.data.split('_')[1]


bot.polling()

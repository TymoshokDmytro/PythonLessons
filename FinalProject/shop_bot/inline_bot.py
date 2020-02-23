from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle

from FinalProject.shop_bot.config import TOKEN
from FinalProject.shop_bot.keyboards import START_KB

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    buttons = START_KB.values()
    kb = InlineKeyboardMarkup()

    inline_buttons = [InlineKeyboardButton(text=button, switch_inline_query_current_chat=button) for button in buttons]

    kb.add(*inline_buttons)
    bot.send_message(message.chat.id, 'text', reply_markup=kb)


@bot.inline_handler(func=lambda query: True)
def inline(query):
    results = []
    for i in range(10):
        kb = InlineKeyboardMarkup()

        button = types.InlineKeyboardButton(text='Добавить в корзину', callback_data=str(i))

        kb.add(button)

        result1 = InlineQueryResultArticle(
            id=i + 1,
            title=f'Название{i+1}',
            description=f'Описание{i+1}',
            # input_message_content=types.InputTextMessageContent(message_text='Текст после нажатия на инайн кнопку',                                                                ),
            # input_message_content=types.InputMediaPhoto(
            #     media='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTn8DQPz__lgLXqLR__jYIqOqt-4g4AC56kcc2hrbSUva4Ucnvo',
            #     caption='Описание'
            # ),
            input_message_content=types.InputTextMessageContent(message_text='1'),
            thumb_url='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTn8DQPz__lgLXqLR__jYIqOqt-4g4AC56kcc2hrbSUva4Ucnvo',
            reply_markup=kb

        )
        results.append(result1)

    bot.answer_inline_query(query.id, results, cache_time=0)


@bot.chosen_inline_handler(func=lambda chosen_result: True)
def chosen_result(chosen_result):
    print(chosen_result)


bot.polling()

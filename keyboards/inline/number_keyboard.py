from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


number_inline_keyboard = InlineKeyboardMarkup(row_width=2)
me_button = InlineKeyboardButton(text='Men', callback_data='me')
ketti_button = InlineKeyboardButton(text="Kod ketti", callback_data='ketti')
already_voted_button = InlineKeyboardButton(
    text='Ilgari ovoz berilgan', callback_data='already_voted')

number_inline_keyboard.add(me_button, ketti_button)


after_inline_keyboard = InlineKeyboardMarkup(row_width=2)
voted_button = InlineKeyboardButton(text="O'tdi", callback_data='voted')
already_voted_button = InlineKeyboardButton(
    text="Kod noto'g'ri", callback_data='wrong_code')
after_inline_keyboard.add(me_button, voted_button, already_voted_button)

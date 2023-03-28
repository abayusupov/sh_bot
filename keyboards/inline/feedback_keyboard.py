from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


feedback_inline_keyboard = InlineKeyboardMarkup(row_width=2)
gone_button = InlineKeyboardButton(text='Kod ketti', callback_data='ketti')
already_voted_button = InlineKeyboardButton(
    text='Ilgari ovoz berilgan', callback_data='already_voted')
feedback_inline_keyboard.add(gone_button, already_voted_button)


after_feedback_inline_keyboard = InlineKeyboardMarkup(row_width=2)
voted_button = InlineKeyboardButton(text="O'tdi", callback_data='voted')
wrong_code_button = InlineKeyboardButton(
    text="Kod noto'g'ri", callback_data='wrong_code')
after_feedback_inline_keyboard.add(voted_button, wrong_code_button)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


pay_keyboard = InlineKeyboardMarkup(row_width=1)
pay_button = InlineKeyboardButton(text="To'landi", callback_data='pay')

pay_keyboard.add(pay_button)

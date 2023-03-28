from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


code_state_keyboard = InlineKeyboardMarkup(row_width=1)
ok_button = InlineKeyboardButton(text='OK', callback_data='passtocode')

code_state_keyboard.add(ok_button)


finish_state_keyboard = InlineKeyboardMarkup(row_width=2)
new_number_button = InlineKeyboardButton(
    text='Boshqa raqam kiritish', callback_data='newshare')
share_button = InlineKeyboardButton(
    text="Boshqalarga jo'natish", switch_inline_query="Open budgetda ovoz bering va paynetga ega bo'ling!")

finish_state_keyboard.add(new_number_button, share_button)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


donate_inline_keyboard = InlineKeyboardMarkup(row_width=2)
savob_button = InlineKeyboardButton(text='Faqat savob', callback_data='savob')
paynet_button = InlineKeyboardButton(
    text="Savob va paynet", callback_data='paynet')


donate_inline_keyboard.add(savob_button, paynet_button)

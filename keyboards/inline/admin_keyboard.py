from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


admin_inline_keyboard = InlineKeyboardMarkup(row_width=1)
not_paid_button = InlineKeyboardButton(
    text="To'lanmagan raqamlarni ko'rish", callback_data='not_paid')
paid_button = InlineKeyboardButton(
    text="To'langan raqamlarni ko'rish", callback_data='paid')
not_paid_button_for_pay = InlineKeyboardButton(
    text="To'lanmagan raqamlarni to'lash uchun ko'rish", callback_data='not_paid_for_pay')
count_all_button = InlineKeyboardButton(
    text="Barcha ovozlar soni", callback_data='count_all')
count_all_paynet_button = InlineKeyboardButton(
    text="Pullik ovozlar soni", callback_data='count_all_paynet')
count_all_donate_button = InlineKeyboardButton(
    text="Barcha tekin ovozlar soni", callback_data='count_all_donate')
count_all_not_paid_button = InlineKeyboardButton(
    text="Barcha to'lanmaganlar soni", callback_data='count_all_not_paid')
count_all_paid_button = InlineKeyboardButton(
    text="Barcha to'langan ovozlar soni", callback_data='count_all_paid')
hisobot_button = InlineKeyboardButton(
    text="Umumiy hisobot", callback_data='hisobot')


admin_inline_keyboard.add(not_paid_button, paid_button, not_paid_button_for_pay, count_all_button,
                          count_all_paynet_button, count_all_donate_button, count_all_not_paid_button, count_all_paid_button, hisobot_button)

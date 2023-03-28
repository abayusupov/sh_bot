import asyncio

from aiogram import types

from data.config import ADMINS
from loader import dp, db, bot
from keyboards.inline.admin_keyboard import admin_inline_keyboard
from keyboards.inline.pay_keyboard import pay_keyboard


@dp.message_handler(text="/admin", user_id=ADMINS, state='*')
async def send_ad_to_all(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id, text="Quyidagi tugmalar yordamida kerakli ma'lumotlarni olishingiz mumkin", reply_markup=admin_inline_keyboard)
    # users = await db.select_all_users()
    # for user in users:
    #     # print(user[3])
    #     user_id = user[3]
    #     await asyncio.sleep(0.05)


@dp.callback_query_handler(lambda c: c.data in ['not_paid', 'paid', 'not_paid_for_pay', 'count_all', 'count_all_paynet', 'count_all_donate', 'count_all_not_paid', 'count_all_paid', 'hisobot'], user_id=ADMINS, state='*')
async def admin_method(callback_query: types.CallbackQuery):

    admin_id = callback_query.from_user.id

    data = callback_query.data
    if data == 'not_paid':
        rows = await db.select_all_not_paid_numbers_with_time()
        d = [dict(row) for row in rows]
        for r in d:
            await callback_query.message.answer(f"{r['phone_number']} {r['datetime']}")
            await asyncio.sleep(0.05)
    elif data == 'paid':
        rows = await db.select_all_paid_numbers()
        d = [dict(row)['phone_number'] for row in rows]
        for r in d:
            await callback_query.message.answer(f"{r}")
            await asyncio.sleep(0.05)
    elif data == 'not_paid_for_pay':
        rows = await db.select_all_not_paid_numbers()
        d = [dict(row)['phone_number'] for row in rows]
        for r in d:
            await bot.send_message(chat_id=admin_id, text=f"{r}", reply_markup=pay_keyboard)
            await asyncio.sleep(0.05)
    elif data == 'count_all':
        count = await db.count_all_numbers()
        await bot.send_message(chat_id=admin_id, text=f"Barcha ovozlar soni: {count}")
    elif data == 'count_all_paynet':
        count = await db.count_paynetga_numbers()
        await bot.send_message(chat_id=admin_id, text=f"Barcha pullik ovozlar soni: {count}")
        await callback_query.answer()
    elif data == 'count_all_donate':
        count = await db.count_savobga_numbers()
        await bot.send_message(chat_id=admin_id, text=f"Savob uchun berilgan barcha ovozlar soni: {count}")
    elif data == 'count_all_not_paid':
        count = await db.count_all_not_paid_numbers()
        await bot.send_message(chat_id=admin_id, text=f"Haqqi to'lanmagan ovozlar soni: {count}")
        await callback_query.answer()
    elif data == 'count_all_paid':
        count = await db.count_all_paid_numbers()
        await bot.send_message(chat_id=admin_id, text=f"Haqqi to'langan ovozlar soni: {count}")
    else:
        all = await db.count_all_numbers()
        paynetga = await db.count_paynetga_numbers()
        savobga = await db.count_savobga_numbers()
        not_paid = await db.count_all_not_paid_numbers()
        paid = await db.count_all_paid_numbers()

        hisob = [
            f"Barcha ovozlar soni: {all};",
            f"Barcha pullik ovozlar soni: {paynetga};",
            f"Savob uchun berilgan barcha ovozlar soni: {savobga};",
            f"Haqqi to'lanmagan ovozlar soni: {not_paid};",
            f"Haqqi to'langan ovozlar soni: {paid}"
        ]
        hisobot = "\n".join(hisob)

        await bot.send_message(chat_id=admin_id, text=hisobot)

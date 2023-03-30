from aiogram import types
from states.holatlar import Holatlar
from loader import dp, db, bot
from data.config import group_chat_id, narx
from keyboards.inline.feedback_keyboard import feedback_inline_keyboard
from keyboards.inline.ok_buttons import code_state_keyboard, finish_state_keyboard
from keyboards.inline.donate_keyboard import donate_inline_keyboard
from aiogram.dispatcher import FSMContext
from utils.tashtime import getTimeInTashkent


@dp.callback_query_handler(lambda c: c.data == 'me', state='*')
async def me_handler(callback_query: types.CallbackQuery):

    phone_number = callback_query.message.text
    member_id = callback_query.from_user.id

    await db.update_me(member_id, phone_number)

    try:
        await bot.send_message(chat_id=member_id, text=f"{phone_number}", reply_markup=feedback_inline_keyboard)
        await bot.send_message(chat_id=group_chat_id, text=f"{phone_number} ni {callback_query.from_user.full_name} oldi")
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

    except Exception:
        print(f'{callback_query.from_user.full_name} start qilmagan')
        await callback_query.answer(text=f'{callback_query.from_user.full_name} siz botni start qilmagansiz', show_alert=True)
        await bot.send_message(chat_id=group_chat_id, text=f'{callback_query.from_user.full_name} siz botni start qilmagansiz', show_alert=True)


@dp.callback_query_handler(lambda c: c.data in ['ketti', 'already_voted'], state='*')
async def button_handler(query: types.CallbackQuery):
    member_id = query.from_user.id
    phone_number = query.message.text
    is_taken = await db.is_taken(phone_number)
    if is_taken:
        user_id = await db.get_user_id(member_id, phone_number)
    else:
        user_id = await db.get_user_id_temp(phone_number)
    data = query.data

    if data == 'ketti':
        # update the voted status in the database
        # await update_voted_status(user_id, voted=True)
        await bot.send_message(user_id, 'Iltimos, OK tugmasini bosing va OpenBudget tomonidan borgan sms raqamni kiriting', reply_markup=code_state_keyboard)
        # move user to the number state
        if not is_taken:
            await bot.send_message(chat_id=group_chat_id, text=f"{query.from_user.full_name} {phone_number} ga  kod jo'natdi")
        else:
            await bot.send_message(chat_id=member_id, text=f"{phone_number} ga  sms kodni jo'natish haqida so'rov yuborildi")

        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)

    elif data == 'already_voted':
        await bot.send_message(user_id, 'Ushbu raqamdan ilgari ovoz berilgan ekan. Siz boshqa raqam kiritishingiz mumkin.', reply_markup=finish_state_keyboard)

        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        # move user to the number state
        if not is_taken:
            await bot.send_message(group_chat_id, f'{query.from_user.full_name} {phone_number} raqamini ilgari kiritilgan deb belgiladi.')
        else:
            await bot.send_message(member_id, f'{phone_number} raqamini ilgari kiritilganligi haqida raqam egasiga xabar berildi.')


@dp.callback_query_handler(lambda c: c.data in ['voted', 'wrong_code'], state='*')
async def after_button_handler(query: types.CallbackQuery):
    member_id = query.from_user.id
    code = int(query.message.text.split(":")[1].strip())
    user_id = await db.get_user_id_using_code(code)
    phone_number = await db.get_phone_number_using_code(code)
    is_taken = await db.is_taken_using_code(code)

    if user_id and phone_number:

        data = query.data

        if data == 'voted':
            # update the voted status in the database
            # await update_voted_status(user_id, voted=True)
            datetime = getTimeInTashkent()
            donate = await db.get_donate_using_code(code)
            await db.add_number(phone_number, user_id, datetime, False, donate)
            
            if not donate:
                await bot.send_message(user_id, "Tabriklaymiz, siz muvaffaqiyatli ovoz berdingiz. Hisobingiz yaqin fursatlarda to'ldiriladi.", reply_markup=finish_state_keyboard)
            else:
                await bot.send_message(user_id, "Katta rahmat, siz muvaffaqiyatli ovoz berdingiz. Yo'limizning yaxshilanishiga yordam berganingizda minnatdormiz!.", reply_markup=finish_state_keyboard)
            # move user to the number state

            await bot.send_message(group_chat_id, f'{query.from_user.full_name} {phone_number} raqamini muvaffaqiyatli kiritdi')

        elif data == 'wrong_code':
            await bot.send_message(user_id, "Siz jo'natgan kod mos kelmayapti. Iltimos kodni tekshirib, qaytadan jo'nating")
            if not is_taken:
                await bot.send_message(chat_id=group_chat_id, text=f"{query.from_user.full_name} {phone_number} ga  boshqa kod jo'natish haqida so'rov yubordi")
            else:
                await bot.send_message(chat_id=member_id, text=f"{phone_number} ga  sms kodni jo'natish haqida so'rov yuborildi")

        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        # move user to the code state
    else:
        print('eski kod tugmasi')


@dp.callback_query_handler(lambda c: c.data == 'passtocode', state='*')
async def pass_to_code_handler(callback_query: types.CallbackQuery):
    await Holatlar.code.set()


@dp.callback_query_handler(lambda c: c.data == 'newshare', state='*')
async def new_share_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await Holatlar.donate.set()
    user_id = callback_query.from_user.id
    await bot.send_message(user_id, "Maqsadni tanlagan holda davom etishingiz mumkin",
                           reply_markup=donate_inline_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'pay', state='*')
async def pass_to_code_handler(callback_query: types.CallbackQuery):
    phone_number = callback_query.message.text
    try:
        await db.update_payment(phone_number)
        user_id = await db.get_user_id_using_phone(phone_number)
        await bot.send_message(chat_id=user_id, text=f"{phone_number} raqamiga {narx} so'm o'tkazildi")
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    except Exception:
        print('update paymentda xatolik')

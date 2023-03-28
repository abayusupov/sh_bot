from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from states.holatlar import Holatlar
from loader import dp
from aiogram.dispatcher import FSMContext
from keyboards.inline.donate_keyboard import donate_inline_keyboard


@dp.callback_query_handler(lambda c: c.data in ['savob', 'paynet'], state=Holatlar.donate)
async def bot_choose_method(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['donate'] = callback_query.data

    await Holatlar.phone.set()
    await callback_query.message.answer("Iltimos, telefon raqamingizni kiriting, \nRaqamni: \n+998931234567, \n998971234567, \n981234567 \nkabi formatlarda kiritishingiz mumkin")


@dp.message_handler(state=Holatlar.donate)
async def bad_text_method(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing", reply_markup=donate_inline_keyboard)

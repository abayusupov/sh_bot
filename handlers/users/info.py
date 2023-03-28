from loader import dp, db, bot
from aiogram import types


@dp.message_handler(commands=['info'], state='*')
async def start_handler(message: types.Message):
    await message.answer('Tashabbusli budjet bu tashabbusli budjetdir')

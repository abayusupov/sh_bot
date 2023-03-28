from aiogram.dispatcher.filters.state import State, StatesGroup


class Holatlar(StatesGroup):
    donate = State()
    phone = State()
    wait = State()
    code = State()

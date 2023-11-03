from aiogram.fsm.state import StatesGroup, State


class RouletteState(StatesGroup):
    limit = State()

from aiogram.fsm.state import StatesGroup, State


class MailingState(StatesGroup):
    status = State()

from aiogram.fsm.state import StatesGroup, State


# Машина состояний для входа
class SignInState(StatesGroup):
    login = State()
    password = State()

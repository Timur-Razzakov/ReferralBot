from aiogram.fsm.state import StatesGroup, State


# Машина состояний для регистрации
class AuthState(StatesGroup):
    username = State()
    phone_number = State()
    pay_id = State()
    user_password = State()
    user_password_2 = State()

from aiogram.fsm.state import StatesGroup, State


# Машина состояний для функции забыли пароль
class ForgotPasswordState(StatesGroup):
    user_binance_id = State()
    new_password = State()
    new_password_2 = State()

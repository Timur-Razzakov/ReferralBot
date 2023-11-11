from aiogram.fsm.state import StatesGroup, State


# Машина состояний для функции забыли пароль
class ForgotPasswordState(StatesGroup):
    user_pay_id = State()
    new_password = State()
    new_password_2 = State()

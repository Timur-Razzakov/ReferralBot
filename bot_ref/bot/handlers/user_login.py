from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import check_password

from bot_ref.bot.dataclasses import admins_id
from bot_ref.bot.keyboards import default_kb, admin_kb
from bot_ref.bot.keyboards import registration_kb
from bot_ref.bot.states import SignInState
from bot_ref.bot.utils import get_user_for_login, get_user, paid_check
from bot_ref.models import User

sign_in_router = Router(name=__name__)

SIGN_IN_TEXT = """
Вход был успешно выполнен ⭐️

Для использования функционала бота вам необходимо внести единовременный взнос в размере 100$
После оплаты пожалуйста нажмите кнопку Оплатил 🤑
"""


@sign_in_router.message(F.text == 'Войти 👋')
async def command_sign_in(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите свой Pay_Id ✨",
        reply_markup=registration_kb.markup
    )
    await state.set_state(SignInState.login)


@sign_in_router.message(F.text == 'Помощь 🆘')
async def user_help(message: types.Message):
    help_text = """
    Хотите узнать, как начать зарабатывать с нашим ботом? Вот шаги для регистрации:

Нажмите Регистрация ✌️ и введите ваш Binance Pay ID, имя и номер телефона.
Создайте пароль и подтвердите его, чтобы обеспечить безопасность вашего аккаунта.
После регистрации, используйте Войти👋 и начните свой путь к заработку!
Функционал бота включает в себя приглашение рефералов и вознаграждение за каждого приглашенного. Следите за вашим балансом и собирайте награды!

Если у вас возникли какие-либо вопросы или вам нужна дополнительная помощь, не стесняйтесь обращаться к нам @Podderlka. Мы всегда готовы помочь!
    """
    await message.answer(help_text)


@sign_in_router.message(SignInState.login)
async def process_sign_in(message: types.Message, state: FSMContext):
    pay_id = message.text
    user_id = message.chat.id
    user = await get_user(pay_id=pay_id)

    if user and user.user_id == user_id:
        user = await get_user_for_login(user_id)
        user.pay_id = pay_id
        user.user_id = user_id
        await message.answer(
            "Теперь вам нужно ввести пароль 🔐",
            reply_markup=registration_kb.markup_cancel_forgot_password
        )
        await state.set_state(SignInState.password)
    else:
        await message.answer(
            "Такого логина <b>нет</b>, повторите еще раз ❌",
            reply_markup=registration_kb.markup
        )
        await state.set_state(SignInState.login)


@sign_in_router.message(SignInState.password)
async def process_pass(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    password = message.text
    user = await get_user_for_login(user_id)
    user.password = password
    user.current_state = True

    if await get_password(pay_id=user.pay_id, password=user.password):
        markup = default_kb.paid_kb

        if user_id in admins_id:
            markup = admin_kb.admin_markup
        elif await paid_check(user_id):
            markup = default_kb.markup

        await message.answer(
            SIGN_IN_TEXT,
            reply_markup=markup
        )

        await state.clear()
    else:
        await message.answer(
            "Пароль <b>не правильный</b> попробуйте еще раз 🔄",
            reply_markup=registration_kb.markup_cancel_forgot_password
        )
        await state.set_state(SignInState.password)


@sync_to_async
def get_password(pay_id, password) -> bool:
    user = User.objects.get(pay_id=pay_id)
    return check_password(password, user.user_password)

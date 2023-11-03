from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import check_password

from bot_ref.bot.dataclasses import admins_id
from bot_ref.bot.handlers.authorization import check_user
from bot_ref.bot.handlers.check_paid import paid_check
from bot_ref.bot.keyboards import default_kb, admin_kb
from bot_ref.bot.keyboards.registration_kb import markup, markup_cancel_forgot_password
from bot_ref.bot.states import SignInState
from bot_ref.bot.utils import get_user_for_login
from bot_ref.models import User

sign_in_router = Router(name=__name__)


@sign_in_router.message(F.text == 'Войти 👋')
async def command_sign_in(message: types.Message, state: FSMContext):
    await message.answer("Введите свой Pay_id ✨", reply_markup=markup)
    await state.set_state(SignInState.login)


@sign_in_router.message(SignInState.login)
async def process_sign_in(message: types.Message, state: FSMContext):
    binance_id = message.text
    # проверяем есть ли такое пользователь с указанным binance_id
    if await check_user(binance_id):
        user_id = message.chat.id
        user = await get_user_for_login(user_id)
        user.binance_id = binance_id
        user.user_id = user_id
        await message.answer("Теперь тебе нужно ввести пароль 🔐", reply_markup=markup_cancel_forgot_password)
        await state.set_state(SignInState.password)
    else:
        await message.answer("Такого логина <b>нет</b>, повторите еще раз ❌", reply_markup=markup)
        await state.set_state(SignInState.login)


@sign_in_router.message(SignInState.password)
async def process_pass(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    password = message.text
    user = await get_user_for_login(user_id)
    user.password = password
    user.current_state = True

    if await get_password(binance_id=user.binance_id, password=user.password):
        if user_id in admins_id:
            await message.answer(
                'Вход был <b>успешно</b> выполнен ⭐️',
                reply_markup=admin_kb.admin_markup
            )
        elif await paid_check(user_id):
            await message.answer(
                "Вход был <b>успешно</b> выполнен ⭐️",
                reply_markup=default_kb.markup
            )
        else:
            await message.answer(
                "Вход был <b>успешно</b> выполнен ⭐️",
                reply_markup=default_kb.paid_kb
            )

        await state.clear()

    else:
        await message.answer(
            "Пароль <b>не правильный</b> попробуйте еще раз 🔄",
            reply_markup=markup_cancel_forgot_password
        )
        await state.set_state(SignInState.password)


@sync_to_async
def get_password(binance_id, password):
    user = User.objects.get(binance_id=binance_id)
    if check_password(password, user.user_password):
        return True
    else:
        return False

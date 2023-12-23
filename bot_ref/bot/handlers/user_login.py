from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import check_password

from bot_ref.bot.dataclasses import admins_id
from bot_ref.bot.keyboards import default_kb, admin_kb
from bot_ref.bot.keyboards import registration_kb
from bot_ref.bot.states import SignInState
from bot_ref.bot.texts import payment_text, sign_in_text, input_pay_id_text, help_text, input_password_text, \
    login_error_text, input_password_error_text
from bot_ref.bot.utils import get_user_for_login, get_user, paid_check, clear_state
from bot_ref.models import User

sign_in_router = Router(name=__name__)


@sign_in_router.message(F.text == 'Войти 👋')
async def command_sign_in(message: types.Message, state: FSMContext):
    await clear_state(state)
    await message.answer(
        input_pay_id_text,
        reply_markup=registration_kb.markup
    )
    await state.set_state(SignInState.login)


@sign_in_router.message(F.text == 'Помощь 🆘')
async def user_help(message: types.Message):
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
            input_password_text,
            reply_markup=registration_kb.markup_cancel_forgot_password
        )
        await state.set_state(SignInState.password)
    else:
        await message.answer(
            login_error_text,
            reply_markup=registration_kb.markup
        )
        await state.set_state(SignInState.login)


@sign_in_router.message(SignInState.password)
async def process_pass(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    password = message.text
    user = await get_user_for_login(user_id)
    user.password = password

    if await get_password(pay_id=user.pay_id, password=user.password):
        markup = default_kb.paid_kb
        user.current_state = True

        if user_id in admins_id:
            markup = admin_kb.admin_markup
        elif await paid_check(user_id):
            markup = default_kb.markup

        await message.answer(
            sign_in_text,
            reply_markup=markup
        )
        if not await paid_check(user_id) and user_id not in admins_id:
            await message.answer(
                payment_text
            )

        await state.clear()
    else:
        await message.answer(
            input_password_error_text,
            reply_markup=registration_kb.markup_cancel_forgot_password
        )
        await state.set_state(SignInState.password)


@sync_to_async
def get_password(pay_id, password) -> bool:
    user = User.objects.get(pay_id=pay_id)
    return check_password(password, user.user_password)

import re

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from bot_ref.bot.handlers.check_data import check_login_chat_id, update_user_password
from bot_ref.bot.keyboards import sign_inup_kb
from bot_ref.bot.keyboards.registration_kb import markup
from bot_ref.bot.states import ForgotPasswordState
from bot_ref.bot.texts import reset_password_pay_id_text, new_password_text, reset_password_error_text, \
    repeat_new_password_text, new_password_error_text, success_password_change_text, password_input_error_text
from bot_ref.bot.utils import get_user_for_update

update_password_router = Router(name=__name__)


@update_password_router.message(F.text == 'Забыли пароль? 🆘')
async def forgot_password(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.clear()

    await message.answer(
        reset_password_pay_id_text,
        reply_markup=markup
    )
    await state.set_state(ForgotPasswordState.user_pay_id)


@update_password_router.message(ForgotPasswordState.user_pay_id)
async def process_forgot_password_login(message: types.Message, state: FSMContext):
    pay_id = message.text
    user_id = message.chat.id
    if await check_login_chat_id(user_pay_id=pay_id, chat_id=user_id):
        # получаем класс для заполнения данными сверяем по user_id
        user_data = await get_user_for_update(user_id)
        user_data.pay_id = pay_id
        await message.answer(
            new_password_text,
            reply_markup=markup
        )

        await state.set_state(ForgotPasswordState.new_password)
    else:
        await message.answer(
            reset_password_error_text,
            reply_markup=sign_inup_kb.markup
        )
        await state.clear()


@update_password_router.message(ForgotPasswordState.new_password)
async def process_forgot_password_password(message: types.Message, state: FSMContext):
    password = message.text
    if len(password) > 5 and re.match('^[a-zA-Z0-9]+$', message.text):
        user_id = message.chat.id
        user_data = await get_user_for_update(user_id)
        user_data.new_password = password
        await message.answer(repeat_new_password_text, reply_markup=markup)
        await state.set_state(ForgotPasswordState.new_password_2)
    else:
        await message.answer(new_password_error_text, reply_markup=markup)
        await state.set_state(ForgotPasswordState.new_password)


@update_password_router.message(ForgotPasswordState.new_password_2)
async def process_forgot_password_password_2(message: types.Message, state: FSMContext):
    repeat_password = message.text
    user_id = message.chat.id
    user_data = await get_user_for_update(user_id)
    user_data.repeat_password = repeat_password
    if user_data.new_password == user_data.repeat_password:
        await update_user_password(pay_id=user_data.pay_id,
                                   password=user_data.new_password)
        await state.clear()
        await message.answer(
            success_password_change_text,
            reply_markup=sign_inup_kb.markup
        )
    else:
        await message.answer(password_input_error_text, reply_markup=markup)
        await state.set_state(ForgotPasswordState.new_password)

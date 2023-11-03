import re

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from bot_ref.bot.handlers.check_data import check_login_chat_id, update_user_password
from bot_ref.bot.keyboards import sign_inup_kb
from bot_ref.bot.keyboards.registration_kb import markup
from bot_ref.bot.states import ForgotPasswordState
from bot_ref.bot.utils import get_user_for_update

update_password_router = Router(name=__name__)


@update_password_router.message(F.text == 'Забыли пароль? 🆘')
async def forgot_password(message: types.Message, state: FSMContext):
    await message.answer("Чтобы изменить пароль, для начала введите ваш binance_id 🫡", reply_markup=markup)
    await state.set_state(ForgotPasswordState.user_binance_id)


@update_password_router.message(ForgotPasswordState.user_binance_id)
async def process_forgot_password_login(message: types.Message, state: FSMContext):
    binance_id = message.text
    user_id = message.chat.id
    if await check_login_chat_id(user_binance_id=binance_id, chat_id=user_id):
        # получаем класс для заполнения данными сверяем по user_id
        user_data = await get_user_for_update(user_id)
        user_data.binance_id = binance_id
        await message.answer("binance_id <b>успешно</b> найден, "
                             "и ID пользователя совпадает с логином 🌟\n\n "
                             "Теперь вы <b>сможете</b> изменить пароль ✅\n\n"
                             "Введите <b>новый пароль</b> ✍️", reply_markup=markup)

        await state.set_state(ForgotPasswordState.new_password)
    else:
        await message.answer("Вы <b>не прошли проверку</b> ❌\n\n"
                             "На это могут быть две причины:\n"
                             "1. Такого логина нет\n"
                             "2. Ваш ID пользователя не совпадает с binance_id который вы указали\n\n"
                             "Вы можете <b>повторить</b> попытку 🔄",
                             reply_markup=sign_inup_kb.markup)
        await state.clear()


@update_password_router.message(ForgotPasswordState.new_password)
async def process_forgot_password_password(message: types.Message, state: FSMContext):
    password = message.text
    if len(password) > 5 and re.match('^[a-zA-Z0-9]+$', message.text):
        user_id = message.chat.id
        user_data = await get_user_for_update(user_id)
        user_data.new_password = password
        await message.answer("Введи пароль <b>еще раз</b> 🔄", reply_markup=markup)
        await state.set_state(ForgotPasswordState.new_password_2)
    else:
        await message.answer("Пароль должен быть только из <b>латинских букв</b> "
                             "и содержать хотя бы <b>одну цифру</b>\n\n"
                             "Повторите попытку 🔄", reply_markup=markup)
        await state.set_state(ForgotPasswordState.new_password)


@update_password_router.message(ForgotPasswordState.new_password_2)
async def process_forgot_password_password_2(message: types.Message, state: FSMContext):
    repeat_password = message.text
    user_id = message.chat.id
    user_data = await get_user_for_update(user_id)
    user_data.repeat_password = repeat_password
    if user_data.new_password == user_data.repeat_password:
        await update_user_password(binance_id=user_data.binance_id,
                                   password=user_data.new_password)
        await state.clear()
        await message.answer("Изменение пароля прошла <b>успешно</b> ✅\n\n"
                             "Теперь, войдите в свой профиль 💝",
                             reply_markup=sign_inup_kb.markup)
    else:
        await message.answer("Вы ввели пароль <b>не правильно</b> ❌\n\n"
                             "Попробуйте еще раз 🔄", reply_markup=markup)
        await state.set_state(ForgotPasswordState.new_password)

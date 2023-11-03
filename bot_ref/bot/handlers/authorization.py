import re

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from bot_ref.bot.handlers.check_data import check_user_chat_id, check_user
from bot_ref.bot.keyboards import sign_inup_kb
from bot_ref.bot.keyboards.registration_kb import markup
from bot_ref.bot.loader import bot
from bot_ref.bot.states import AuthState
from bot_ref.bot.utils import get_user_for_registration, save_user, get_user, create_referral, get_user_referral

sign_up_router = Router(name=__name__)

REGISTRATION_TEXT = """
Для регистрации сначала напишите свой binance_id!

Из чего должен состоять Pay_id?
    - Pay_id должен состоять только из <b>цифр</b>!
    - Длинна Pay_id должна быть <b>больше 3 символов(цифр)</b>
    - Pay_id должен быть <b>уникальным и не повторяющимися</b>

Перед тем как отравить логин перепроверьте его!
"""



@sign_up_router.message(F.text == 'Отмена ❌')
async def command_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(text="Операция успешно отменена 🙅‍", reply_markup=sign_inup_kb.markup)


@sign_up_router.message(F.text == 'Регистрация ✌️')
async def process_registration(message: types.Message, state: FSMContext):
    await message.answer(REGISTRATION_TEXT, reply_markup=markup)
    await state.set_state(AuthState.binance_id)


@sign_up_router.message(AuthState.binance_id)
async def process_binance_id(message: types.Message, state: FSMContext):
    binance_id = message.text
    user_id = message.chat.id
    user = await get_user_for_registration(user_id)
    if await check_user_chat_id(chat_id=user_id):
        await message.answer("Пользователь с таким ID как у вас уже есть, войдите в свой аккаунт 🫡",
                             reply_markup=sign_inup_kb.markup)
    else:
        if await check_user(binance_id=binance_id):
            await message.answer(
                "Пользователь с таким binance_id <b>уже есть</b>, попробуйте еще раз ↩️",
                reply_markup=markup)
            await state.set_state(AuthState.binance_id)
        else:
            if re.match('^[0-9]+$', binance_id) and len(binance_id) > 3:
                user.binance_id = binance_id
                await message.answer("Теперь напиши ваше имя ✍️", reply_markup=markup)
                await state.set_state(AuthState.username)
            else:
                await message.answer("Pay_id должен состоять только из <b>цифр 🔢</b>\n\n"
                                     "Попробуйте еще раз ↩️!", reply_markup=markup)
                await state.set_state(AuthState.binance_id)


@sign_up_router.message(AuthState.username)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text
    user_id = message.chat.id
    user = await get_user_for_registration(user_id)
    user.user_name = username
    await message.answer("Ваш номер телефона?✍️", reply_markup=markup)
    await state.set_state(AuthState.phone_number)


@sign_up_router.message(AuthState.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    user_id = message.chat.id
    user = await get_user_for_registration(user_id)
    user.phone_number = phone_number
    await message.answer("Теперь напиши пароль ✍️", reply_markup=markup)
    await state.set_state(AuthState.user_password)


@sign_up_router.message(AuthState.user_password)
async def process_password(message: types.Message, state: FSMContext):
    password = message.text
    if len(password) > 5 and re.match('^[a-zA-Z0-9]+$', password):
        user_id = message.chat.id
        user = await get_user_for_registration(user_id)
        user.user_password = password
        user.user_id = user_id
        # получаем имя бота
        user.bot_name = (await bot.get_me()).username
        await message.answer("Введи пароль <b>еще раз</b> 🔄", reply_markup=markup)
        await state.set_state(AuthState.user_password_2)
    else:
        await message.answer("Пароль должен быть только из <b>латинских букв</b> "
                             "и содержать хотя бы <b>одну цифру</b>\n\n"
                             "Повторите попытку 🔄", reply_markup=markup)
        await state.set_state(AuthState.user_password)


@sign_up_router.message(AuthState.user_password_2)
async def process_password_2(message: types.Message, state: FSMContext):
    password_2 = message.text
    user_id = message.chat.id
    user = await get_user_for_registration(user_id)
    user.repeat_password = password_2
    if user.user_password == user.repeat_password:

        referrals = await get_user_referral(user_id)
        if referrals.sender_link_id and referrals.user_id:
            # получаем пользователей через user_id
            referrer = await get_user(referrals.sender_link_id)

            await save_user(
                binance_id=user.binance_id,
                user_password=user.user_password,
                user_id=user.user_id,
                user_name=user.user_name,
                phone_number=user.phone_number,
                bot_name=user.bot_name,
                referrer_id=referrer.pk
            )

            referral = await get_user(referrals.user_id)
            await create_referral(referrer.pk, referral)
            await state.clear()
            await bot.send_message(referrals.sender_link_id,
                                   text=f'У вас появился реферал по имени: {referrer.user_name}')
        await message.answer("Регистрация прошла <b>успешно</b> ✅\n\n"
                             "Теперь, Вы должны оплатить начальный взнос 💝",
                             reply_markup=sign_inup_kb.markup)
    else:
        await message.answer("Вы ввели пароль <b>не правильно</b> ❌\n\n"
                             "Попробуйте еще раз 🔄", reply_markup=markup)
        await state.set_state(AuthState.user_password)

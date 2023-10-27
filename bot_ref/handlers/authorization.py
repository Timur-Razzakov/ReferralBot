import re

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password
from django.db import transaction

from bot_ref.handlers.check_data import my_router, check_user_chat_id, check_user
from bot_ref.handlers.default import get_user_referral
from bot_ref.handlers.referral import get_user, create_referral
from bot_ref.keyboards import sign_inup_kb
from bot_ref.keyboards.registration_kb import markup
from bot_ref.loader import bot
from bot_ref.models import User
from bot_ref.states import AuthState


class UserData:
    def __init__(self):
        self.user_id = None
        self.binance_id = None
        self.user_name = None
        self.phone_number = None
        self.invite_link = None
        self.user_password = None
        self.repeat_password = None
        self.bot_name = None


# Сделан хендлер авторизации
users = {}

REGISTRATION_TEXT = """
Для регистрации сначала напишите свой binance_id!

Из чего должен состоять Pay_id?
    - Pay_id должен состоять только из <b>цифр</b>!
    - Длинна Pay_id должна быть <b>больше 3 символов(цифр)</b>
    - Pay_id должен быть <b>уникальным и не повторяющимися</b>

Перед тем как отравить логин перепроверьте его!
"""


# Создаем функцию для инициализации user_order
@sync_to_async
def get_user_for_registration(user_id):
    if user_id not in users:
        users[user_id] = UserData()
    return users[user_id]


async def command_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(text="Операция успешно отменена 🙅‍", reply_markup=sign_inup_kb.markup)


@my_router.message(F.text == 'Регистрация ✌️')
async def process_registration(message: types.Message, state: FSMContext):
    await message.answer(REGISTRATION_TEXT, reply_markup=markup)
    await state.set_state(AuthState.binance_id)


@my_router.message(AuthState.binance_id)
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


@my_router.message(AuthState.username)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text
    user_id = message.chat.id
    user = await get_user_for_registration(user_id)
    user.user_name = username
    await message.answer("Ваш номер телефона?✍️", reply_markup=markup)
    await state.set_state(AuthState.phone_number)


@my_router.message(AuthState.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    user_id = message.chat.id
    user = await get_user_for_registration(user_id)
    user.phone_number = phone_number
    await message.answer("Теперь напиши пароль ✍️", reply_markup=markup)
    await state.set_state(AuthState.user_password)


@my_router.message(AuthState.user_password)
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


@my_router.message(AuthState.user_password_2)
async def process_password_2(message: types.Message, state: FSMContext):
    password_2 = message.text
    user_id = message.chat.id
    user = await get_user_for_registration(user_id)
    user.repeat_password = password_2
    if user.user_password == user.repeat_password:

        await save_user(binance_id=user.binance_id,
                        user_password=user.user_password,
                        user_id=user.user_id,
                        user_name=user.user_name,
                        phone_number=user.phone_number,
                        bot_name=user.bot_name)
        referrals = await get_user_referral(user_id)
        if referrals.sender_link_id and referrals.user_id:
            # получаем пользователей через user_id
            user = await get_user(referrals.sender_link_id)
            referral = await get_user(referrals.user_id)
            await create_referral(user.pk, referral)
            await state.clear()
            await bot.send_message(referrals.sender_link_id,
                                   text=f'У вас появился реферал по имени: {user.user_name}')
        await message.answer("Регистрация прошла <b>успешно</b> ✅\n\n"
                             "Теперь, Вы должны оплатить начальный взнос 💝",
                             reply_markup=sign_inup_kb.markup)
    else:
        await message.answer("Вы ввели пароль <b>не правильно</b> ❌\n\n"
                             "Попробуйте еще раз 🔄", reply_markup=markup)
        await state.set_state(AuthState.user_password)


@sync_to_async
@transaction.atomic
def save_user(binance_id, user_password, user_id, user_name, phone_number, bot_name):
    user = User.objects.create(binance_id=binance_id,
                               user_password=make_password(user_password),
                               is_registered=True,
                               is_active=False,
                               user_id=user_id,
                               invite_link=f"https://t.me/{bot_name}?start={user_id}",
                               user_name=user_name,
                               phone_number=phone_number)
    return user


def authorization_handlers_register(router: Router) -> None:
    router.message.register(command_cancel, F.text == 'Отмена ❌', )
    router.message.register(process_registration, F.text == 'Регистрация ✌️', )
    router.message.register(process_binance_id, AuthState.binance_id)
    router.message.register(process_username, AuthState.username)
    router.message.register(process_phone_number, AuthState.phone_number)
    router.message.register(process_password, AuthState.user_password)
    router.message.register(process_password_2, AuthState.user_password_2)

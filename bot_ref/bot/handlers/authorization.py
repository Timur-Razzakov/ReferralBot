import re

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from bot_ref.bot.handlers.check_data import check_user_chat_id, check_user
from bot_ref.bot.keyboards import registration_kb
from bot_ref.bot.keyboards import sign_inup_kb
from bot_ref.bot.loader import bot
from bot_ref.bot.states import AuthState
from bot_ref.bot.utils import get_user_for_registration, save_user, get_user, create_referral, get_user_referral
from config import settings

sign_up_router = Router(name=__name__)

REGISTRATION_TEXT = """
Для регистрации сначала напишите свой Binance Pay_Id!
❔Подробную информацию о том что из себя представляет Pay_Id и где его искать вы найдете на официальном сайте Binance: 
https://www.binance.com/ru/support/faq/%D0%BA%D0%B0%D0%BA-%D0%BD%D0%B0%D0%B9%D1%82%D0%B8-binance-pay-id-f3040335259a4b1ea68934daf94bab1d

‼️Перед тем как отравить Ваш Pay_Id убедитесь что вы написали его правильно!
"""


@sign_up_router.message(F.text == 'Отмена ❌')
async def command_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.clear()

    await message.answer(
        text="Операция успешно отменена 🙅‍",
        reply_markup=sign_inup_kb.markup
    )


@sign_up_router.message(F.text == 'Регистрация ✌️')
async def process_registration(message: types.Message, state: FSMContext):
    await message.answer(REGISTRATION_TEXT, reply_markup=registration_kb.markup)
    await state.set_state(AuthState.pay_id)


@sign_up_router.message(AuthState.pay_id)
async def process_binance_id(message: types.Message, state: FSMContext):
    pay_id = message.text
    user_id = message.chat.id
    user = await get_user_for_registration(user_id)
    if await check_user_chat_id(chat_id=user_id):
        await message.answer("Пользователь с таким ID как у вас уже есть, войдите в свой аккаунт 🫡",
                             reply_markup=sign_inup_kb.markup)
        await state.clear()
    else:
        if await check_user(pay_id=pay_id):
            await message.answer(
                "Пользователь с таким pay_id <b>уже есть</b>, попробуйте еще раз ↩️",
                reply_markup=registration_kb.markup)
            await state.set_state(AuthState.pay_id)
        else:
            if re.match('^[0-9]+$', pay_id) and len(pay_id) > 3:
                user.pay_id = pay_id
                await message.answer("Теперь напиши ваше имя ✍️", reply_markup=registration_kb.markup)
                await state.set_state(AuthState.username)
            else:
                await message.answer("Pay_id должен состоять только из <b>цифр 🔢</b>\n\n"
                                     "Попробуйте еще раз ↩️!", reply_markup=registration_kb.markup)
                await state.set_state(AuthState.pay_id)


@sign_up_router.message(AuthState.username)
async def process_username(message: types.Message, state: FSMContext):
    phone_number_text = """
    Следующий шаг: отправьте номер Вашего телефона✍️

Важно знать❗️

Мы не пишем, не звоним и храним ваши данные пользователя в конфиденциальности!🔐

Убедительная просьба‼️

Убедитесь, что вы ввели свой рабочий номер телефона! В случае утери пользовательского пароля, восстановление будет возможным только через номер телефона!
Формат номера телефона должно быть полным!📝

Пример: +71234567890  ✅
    """
    username = message.text
    user_id = message.chat.id
    user = await get_user_for_registration(user_id)
    user.user_name = username
    await message.answer(phone_number_text, reply_markup=registration_kb.markup)
    await state.set_state(AuthState.phone_number)


@sign_up_router.message(AuthState.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    user_id = message.chat.id
    user = await get_user_for_registration(user_id)
    user.phone_number = phone_number
    await message.answer(
        "Теперь придумайте и напишите пароль ✍️",
        reply_markup=registration_kb.markup
    )
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
        await message.answer("Введи пароль <b>еще раз</b> 🔄", reply_markup=registration_kb.markup)
        await state.set_state(AuthState.user_password_2)
    else:
        await message.answer("Пароль должен быть только из <b>латинских букв</b> "
                             "и содержать хотя бы <b>одну цифру</b>\n\n"
                             "Повторите попытку 🔄", reply_markup=registration_kb.markup)
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
            referrer = await get_user(user_id=referrals.sender_link_id)

            await save_user(
                pay_id=user.pay_id,
                user_password=user.user_password,
                user_id=user.user_id,
                user_name=user.user_name,
                phone_number=user.phone_number,
                bot_name=user.bot_name,
                referrer_id=referrer.pk
            )

            referral = await get_user(user_id=referrals.user_id)
            await create_referral(referrer.pk, referral)
            await state.clear()
            await bot.send_message(
                referrals.sender_link_id,
                text=f'У вас появился реферал по имени: {referral.user_name}'
            )
            await bot.send_message(
                chat_id=settings.NOTIFICATION_GROUP_ID,
                text=f'Пользователь {referral.user_name}, присоединился по'
                     f'ссылке пользователя {referrer.user_name}'
            )
        await message.answer(
            "Регистрация прошла успешно ✅ \n\n"
            "Теперь Вам нужно зайти в свой аккаунт"
            " с помощью команды Войти 👋",
            reply_markup=sign_inup_kb.markup
        )
    else:
        await message.answer(
            "Вы ввели пароль <b>не правильно</b> ❌\n\n"
            "Попробуйте еще раз 🔄",
            reply_markup=registration_kb.markup
        )
        await state.set_state(AuthState.user_password)

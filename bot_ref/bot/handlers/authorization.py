import re

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from bot_ref.bot.dataclasses import admins_id
from bot_ref.bot.handlers.check_data import check_user_chat_id, check_user
from bot_ref.bot.keyboards import registration_kb, admin_kb
from bot_ref.bot.keyboards import sign_inup_kb
from bot_ref.bot.loader import bot
from bot_ref.bot.states import AuthState
from bot_ref.bot.texts import registration_text, cancel_action_text, user_id_error_text, pay_id_error_text, \
    user_name_text, pay_id_type_error_text, phone_number_text, password_text, retry_password_text, \
    password_letters_error_text, new_referral_text, new_referral_notification_text, registration_success_text, \
    password_error_text, exists_phone_text
from bot_ref.bot.utils import get_user_for_registration, save_user, get_user, create_referral, get_user_referral, \
    check_login, clear_state, phone_exists
from config import settings

sign_up_router = Router(name=__name__)


@sign_up_router.message(F.text == 'Отмена ❌')
async def command_cancel(message: types.Message, state: FSMContext):
    await clear_state(state)
    markup = sign_inup_kb.markup

    if (message.chat.id in admins_id and
            await check_login(message.chat.id)):
        markup = admin_kb.markup

    await message.answer(
        text=cancel_action_text,
        reply_markup=markup
    )


@sign_up_router.message(F.text == 'Регистрация ✌️')
async def process_registration(message: types.Message, state: FSMContext):
    await clear_state(state)
    await message.answer(registration_text, reply_markup=registration_kb.markup)
    await state.set_state(AuthState.pay_id)


@sign_up_router.message(AuthState.pay_id)
async def process_binance_id(message: types.Message, state: FSMContext):
    pay_id = message.text
    user_id = message.chat.id
    user = await get_user_for_registration(user_id)
    if await check_user_chat_id(chat_id=user_id):
        await message.answer(user_id_error_text,
                             reply_markup=sign_inup_kb.markup)
        await state.clear()
    else:
        if await check_user(pay_id=pay_id):
            await message.answer(
                pay_id_error_text,
                reply_markup=registration_kb.markup)
            await state.set_state(AuthState.pay_id)
        else:
            if re.match('^[0-9]+$', pay_id) and len(pay_id) > 3:
                user.pay_id = pay_id
                await message.answer(user_name_text, reply_markup=registration_kb.markup)
                await state.set_state(AuthState.username)
            else:
                await message.answer(pay_id_type_error_text, reply_markup=registration_kb.markup)
                await state.set_state(AuthState.pay_id)


@sign_up_router.message(AuthState.username)
async def process_username(message: types.Message, state: FSMContext):
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
    if phone_exists(phone_number):
        await state.clear()
        await message.answer(
            exists_phone_text,
            reply_markup=sign_inup_kb.markup
        )
        return

    await message.answer(
        password_text,
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
        await message.answer(
            retry_password_text,
            reply_markup=registration_kb.markup
        )
        await state.set_state(AuthState.user_password_2)
    else:
        await message.answer(
            password_letters_error_text,
            reply_markup=registration_kb.markup
        )
        await state.set_state(AuthState.user_password)


@sign_up_router.message(AuthState.user_password_2)
async def process_password_2(
        message: types.Message,
        state: FSMContext
):
    password_2 = message.text
    user_id = message.chat.id
    user = await get_user_for_registration(user_id)
    user.repeat_password = password_2
    if user.user_password == user.repeat_password:

        referrals = await get_user_referral(user_id)
        if not referrals.sender_link_id:
            referrals.sender_link_id = settings.MAIN_ADMIN_ID

        if not referrals.user_id:
            referrals.user_id = user_id

        referrer = await get_user(
            user_id=referrals.sender_link_id
        )

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
            text=new_referral_text.format(user_name=referral.user_name)
        )
        await bot.send_message(
            chat_id=settings.NOTIFICATION_GROUP_ID,
            text=new_referral_notification_text.format(
                referrer_user_name=referrer.user_name,
                referral_user_name=referral.user_name
            )
        )
        await message.answer(
            registration_success_text,
            reply_markup=sign_inup_kb.markup
        )
    else:
        await message.answer(
            password_error_text,
            reply_markup=registration_kb.markup
        )
        await state.set_state(AuthState.user_password)

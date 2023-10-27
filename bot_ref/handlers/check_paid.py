from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from django.contrib.sites import requests

from bot_ref.keyboards import paid_ikb, sign_inup_kb, admin_kb
from bot_ref.loader import bot, dp
from config import settings as config
from .authorization import my_router
from .check_data import update_user_is_active
from .referral import get_user
from ..models import User

@my_router.message(F.text == 'Оплатил 🤑')
async def cmd_check_paid(message: types.Message):
    # user_id = message.chat.id
    # if await check_login(user_id):
    help_text = "<b>Заметка:</b>\n"
    help_text += ('После совершения оплаты, вы должны нажать на эту кнопку. После проверки, '
                  'мы активируем ваш аккаунт!')
    await bot.send_message(chat_id=message.chat.id,
                           text=help_text, reply_markup=paid_ikb.check_paid)
    # else:
    #     await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
    #                          reply_markup=sign_inup_kb.markup)


@dp.callback_query(F.data == "send")
async def send_data(callback_query: types.CallbackQuery):
    admin_chat_id = config.ADMINS
    user_id = await get_user(user_id=callback_query.message.chat.id)
    message_text = ''
    message_text += "<pre>"
    message_text += "{:<15} {:<15} {:<15} {:<15}\n".format(
        "Username", "Pay ID", "User_id", "Paid")
    message_text += "{:<15} {:<15} {:<15} {:<15} \n".format(
        user_id.user_name, user_id.binance_id,
        user_id.user_id, '✅ Yes' if user_id.is_active else '❌ No')
    message_text += "</pre>"
    await send_data_to_admin(admin_chat_id, message_text)
    await callback_query.answer("Данные отправлены админу")


async def send_data_to_admin(admin_chat_id, data_to_send):
    await bot.send_message(admin_chat_id, data_to_send, reply_markup=paid_ikb.pay)


@dp.callback_query(lambda query: query.data in ['reject', 'confirm'])
# Слушаем ответ админа и отправляем клиенту
async def send_to_client(callback_query: types.CallbackQuery, state: FSMContext):
    global user_id
    text = callback_query.message.text
    # костыль, для получения user_id

    lines = text.split('\n')  # Разбиваем текст на строки
    if len(lines) > 1:
        header = lines[0].split()  # Получаем заголовок таблицы
        data = lines[1].split()  # Получаем данные из первой строки таблицы
        if len(data) >= 3:
            user_id = data[2]  # Получаем User_id (третья колонка)

    if callback_query.data == "reject":
        await bot.send_message(user_id, text="Ваша Заявка отклонена🙅‍", reply_markup=admin_kb.markup)
    elif callback_query.data == "confirm":
        await update_user_is_active(user_id)
        await bot.send_message(user_id, text="Ваша заявка подтверждена, Ваш аккаунт полностью доступен!!",
                               reply_markup=admin_kb.markup)

    await state.clear()


def check_paid_handlers_register(router: Router) -> None:
    router.message.register(cmd_check_paid, F.text == 'Оплатил 🤑')

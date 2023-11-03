from aiogram import types, Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from tabulate import tabulate

from bot_ref.bot.keyboards import paid_ikb, default_kb
from bot_ref.bot.loader import bot
from config import settings as config
from .check_data import update_user_is_active
from .referral import get_user
from ..dataclasses import PayConfirmAction, PayConfirmCallback
from ..keyboards import admin_kb
from ..keyboards.default_kb import paid_kb
from ..utils import send_data_to_admin, paid_check

check_paid_router = Router(name=__name__)


@check_paid_router.message(F.text == 'Оплатил 🤑')
async def cmd_check_paid(message: types.Message):
    user_id = message.chat.id
    if await paid_check(user_id):
        await message.answer(
            'Вы уже оплатили взнос 🥳',
            reply_markup=default_kb.markup
        )
    else:
        help_text = "<b>Заметка:</b>\n"
        help_text += ('После совершения оплаты, вы должны нажать на эту кнопку. После проверки, '
                      'мы активируем ваш аккаунт!')
        await message.answer(text=help_text, reply_markup=paid_ikb.check_paid)


@check_paid_router.callback_query(F.data == "send")
async def send_data(callback_query: types.CallbackQuery):
    admin_chat_id = config.ADMINS
    user = await get_user(user_id=callback_query.message.chat.id)
    is_active = '✅ Yes' if user.is_active else '❌ No'
    text = tabulate(
        tabular_data=[[user.user_name, user.binance_id, user.user_id, is_active]],
        headers=['Username', 'Pay ID', 'User_id', 'Paid'],
        tablefmt='pretty'
    )
    html = f'<pre>{text}</pre>'

    await send_data_to_admin(admin_chat_id, html, user.user_id)
    await callback_query.message.edit_text('Данные отправлены админу 👍')
    await callback_query.answer()


@check_paid_router.callback_query(
    PayConfirmCallback.filter(
        (F.action == PayConfirmAction.CONFIRM) |
        (F.action == PayConfirmAction.REJECT)
    )
)
async def send_to_client(
        callback_query: types.CallbackQuery,
        callback_data: CallbackData,
        state: FSMContext
):
    user_id = callback_data.user_id
    message_text = (f'<pre>{callback_query.message.text}</pre>'
                    f'<b>Аккаунт проверен ✅</b>')

    if callback_data.action == PayConfirmAction.REJECT:
        await bot.send_message(
            user_id,
            text="Ваша Заявка отклонена🙅‍",
            reply_markup=paid_kb
        )
        await callback_query.message.edit_text(message_text)
        await callback_query.answer()
    elif callback_data.action == PayConfirmAction.CONFIRM:
        await update_user_is_active(user_id)
        await bot.send_message(
            user_id,
            text="Ваша заявка подтверждена, Ваш аккаунт полностью доступен!!",
            reply_markup=default_kb.markup
        )
        await callback_query.message.edit_text(message_text)
        await callback_query.answer()

    await state.clear()

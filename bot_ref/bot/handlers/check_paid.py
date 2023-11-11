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
from ..keyboards.default_kb import paid_kb
from ..utils import send_data_to_admin, get_payment_status, create_payment_request, update_payment_request
from ...models import RequestStatus

check_paid_router = Router(name=__name__)


@check_paid_router.message(F.text == 'Оплатил 🤑')
async def cmd_check_paid(message: types.Message):
    user_id = message.chat.id

    payment_request = await get_payment_status(user_id)

    if payment_request and payment_request.status == RequestStatus.CONFIRM:
        await message.answer(
            'Вы уже оплатили взнос 🥳',
            reply_markup=default_kb.markup
        )

    if payment_request:
        await message.answer(
            f'Вы уже отправляли заявку на проверку оплаты'
            f'ниже вы можете узнать его статус\n\n'
            f'Статус заявки: {payment_request.status}'
        )
        return
    else:
        help_text = "<b>Заметка:</b>\n"
        help_text += ('После совершения оплаты, вы должны нажать на эту кнопку. После проверки, '
                      'мы активируем ваш аккаунт!')
        user = await get_user(user_id=user_id)
        await create_payment_request(user)
        await message.answer(text=help_text, reply_markup=paid_ikb.check_paid)


@check_paid_router.callback_query(F.data == "send")
async def send_data(callback_query: types.CallbackQuery):
    admin_chat_id = config.MAIN_ADMIN_ID
    user_id = callback_query.message.chat.id
    user = await get_user(user_id=user_id)
    referrer = await get_user(pk=user.referrer_id)

    is_active = '✅ Yes' if user.is_active else '❌ No'
    text = tabulate(
        tabular_data=[
            [user.user_name, user.pay_id, user.user_id, referrer.pay_id, is_active]
        ],
        headers=['username', 'pay_id', 'user_id', 'referrer_id', 'paid'],
        tablefmt='pretty'
    )
    html = f'<pre>{text}</pre>'

    await send_data_to_admin(admin_chat_id, html, user.user_id)
    await callback_query.message.edit_text(
        'Данные отправлены админу 📨 \n\n'
        'Пожалуйста ожидайте верификации аккаунта!'
    )
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

    reject_text = """
    Ваша Заявка отклонена🙅

❗️Если у Вас возникли какие-то проблемы или вопросы, обращайтесь в нашу поддержку @Poderjka
    """

    confirm_text = """
    ✅Ваша заявка подтверждена, добро пожаловать!

Скорее начинайте зарабатывать с нами!
    """

    payment_request = get_payment_status(user_id)

    if callback_data.action == PayConfirmAction.REJECT:
        await bot.send_message(
            user_id,
            text=reject_text,
            reply_markup=paid_kb
        )
        await callback_query.message.edit_text(message_text)
        await update_payment_request(payment_request, RequestStatus.REJECT)
        await callback_query.answer()
    elif callback_data.action == PayConfirmAction.CONFIRM:
        await update_user_is_active(user_id)
        await bot.send_message(
            user_id,
            text=confirm_text,
            reply_markup=default_kb.markup
        )
        await callback_query.message.edit_text(message_text)
        await update_payment_request(payment_request, RequestStatus.CONFIRM)
        await callback_query.answer()

    await state.clear()

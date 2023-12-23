from aiogram import types, F, Router
from tabulate import tabulate

from bot_ref.bot.dataclasses import admins_id
from bot_ref.bot.handlers.check_data import check_active_user
from bot_ref.bot.middlewares.is_paid import IsPaidMiddleware
from bot_ref.bot.texts import referral_text, not_paid_referral_text
from bot_ref.bot.utils import get_user, get_referrals

referral_router = Router(name=__name__)
referral_router.message.middleware(IsPaidMiddleware())


@referral_router.message(F.text == 'Реферальная ссылка 🚀')
async def get_invite_link(message: types.Message):
    user_id = message.chat.id
    if await check_active_user(user_id) or user_id in admins_id:
        user = await get_user(user_id=message.chat.id)
        # await message.answer(f"Ваша реферальная ссылка: {user.invite_link} \n\n")
        await message.answer(referral_text.format(invite_link=user.invite_link))
    else:
        await message.answer(not_paid_referral_text)


@referral_router.message(F.text == 'Мои рефералы')
async def get_my_referrals(message: types.Message):
    user = await get_user(user_id=message.chat.id)
    referral_list = await get_referrals(user.pk)
    referral_headers = ["Username", "Pay ID", "Paid status"]
    referral_rows = [
        [
            referral['username'],
            referral['pay_id'],
            '✅ Yes' if referral['is_active'] else '❌ No'
        ] for referral in referral_list
    ]
    table = tabulate(referral_rows, referral_headers, tablefmt='pretty')
    html = (f'На данный момент у Вас {len(referral_list)} рефералов:'
            f'<pre>{table}</pre>')

    await message.answer(text=html, parse_mode='HTML')

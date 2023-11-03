from aiogram import types, F, Router
from tabulate import tabulate

from bot_ref.bot.handlers.check_data import check_active_user
from bot_ref.bot.utils import get_user, get_referrals

referral_router = Router(name=__name__)


@referral_router.message(F.text == 'Реферальная ссылка 🚀')
async def get_invite_link(message: types.Message):
    if await check_active_user(message.chat.id):
        user = await get_user(message.chat.id)
        await message.answer(f"Ваша реферальная ссылка: {user.invite_link} \n\n")
    else:
        await message.answer(f"Сначала совершите взнос в размере 100$")


@referral_router.message(F.text == 'Мои рефералы')
async def get_my_referrals(message: types.Message):
    user_id = await get_user(message.chat.id)
    referral_list = await get_referrals(user_id.pk)
    referral_headers = ["Username", "Pay ID", "Paid status"]
    referral_rows = [
        [
            referral['username'],
            referral['binance_id'],
            '✅ Yes' if referral['is_active'] else '❌ No'
        ] for referral in referral_list
    ]
    table = tabulate(referral_rows, referral_headers, tablefmt='pretty')
    html = f'<pre>{table}</pre>'

    await message.answer(text=html, parse_mode='HTML')

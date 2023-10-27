from aiogram import types, F, Router
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from bot_ref.handlers.check_data import check_active_user, my_router
from bot_ref.models import User, Referral


@my_router.message(F.text == 'Реферальная ссылка 🚀')
async def get_invite_link(message: types.Message):
    # Получаем реферальную ссылку
    if await check_active_user(message.chat.id):
        user = await get_user(message.chat.id)
        await message.answer(f"Ваша реферальная ссылка: {user.invite_link} \n\n")
    else:
        await message.answer(f"Сначала совершите взнос в размере 100$")


@my_router.message(F.text == 'Мои рефералы')
async def get_my_referrals(message: types.Message):
    # if not await check_active_user(message.chat.id):
    #     await message.answer(f"Сначала совершите взнос в размере 100💲")
    # else:
    user_id = await get_user(message.chat.id)
    referral_list = await get_referrals(user_id.pk)
    #  отображения информации о рефералах

    message_text = "<b>Информация о рефералах:</b>\n"
    message_text += "<pre>"
    message_text += "{:<15} {:<15} {:<10}\n".format("Username", "Pay ID", "Paid")
    for referral in referral_list:
        message_text += "{:<15} {:<15} {:<10}\n".format(referral['username'], referral['binance_id'],
                                                        '✅ Yes' if referral['is_active'] else '❌ No')
    message_text += "</pre>"

    await message.answer(text=message_text)


@sync_to_async
def create_referral(parent_id, referral):
    create_referral = Referral.objects.create(
        user_id=parent_id,
        referral=referral,
    )
    return create_referral


@sync_to_async
def get_users_sync():
    users = User.objects.all()
    users_info = [
        {
            'pk': user.pk,
            'user_id': user.user_id,
            'binance_id': user.binance_id,
            'username': user.user_name,
            'is_active': user.is_active,
            'count_payment': user.number_payments
        }
        for user in users
    ]
    return users_info


@sync_to_async
def get_user(user_id):
    try:
        user = User.objects.get(user_id=user_id)
        return user
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_referrals(user_id):
    # Получить рефералов пользователя
    referrals = Referral.objects.filter(user_id=user_id).select_related('referral')
    # Создайте список словарей с информацией о рефералах
    referral_info = [
        {
            'user_id': referral.referral.user_id,
            'binance_id': referral.referral.binance_id,
            'username': referral.referral.user_name,
            'is_active': referral.referral.is_active
        }
        for referral in referrals
    ]
    return referral_info


@sync_to_async
def get_data(users):
    # Словарь для хранения информации о пользователях и их рефералах
    user_data = {}
    for user in users:
        referrals = Referral.objects.filter(user_id=user.user_id).select_related('referral')
        # Создать список рефералов с их binance_id и user_name
        referral_data = [
            {'binance_id': referral.referral.binance_id,
             'user_name': referral.referral.user_name,
             'is_active': referral.referral.is_active, }
            for referral in referrals
        ]
        # Добавить информацию о пользователе и его рефералах в словарь
        user_data[user.user_id] = {
            'binance_id': user.binance_id,
            'user_name': user.user_name,
            'referrals': referral_data
        }
    return user_data


def referral_handlers_register(router: Router) -> None:
    router.message.register(get_invite_link, F.text == 'Реферальная ссылка 🚀', )
    router.message.register(get_my_referrals, F.text == 'Мои рефералы', )

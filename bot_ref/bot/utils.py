from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q

from bot_ref.bot.dataclasses import global_users, UserData, global_referrals, ReferralData, global_update_data, \
    UserDataUpdatePassword, global_sign_in, UserDataLogin, PayConfirmCallback, PayConfirmAction, admins_id
from bot_ref.bot.loader import bot
from bot_ref.models import User, Referral, PaymentRequest, RequestStatus


async def check_login(user_id):
    user = await get_user_for_login(user_id)
    if user.current_state:
        return True
    else:
        return False


async def clear_state(state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.clear()


@sync_to_async
def get_users_referrals(limit: int = 0):
    users = User.objects.exclude(
        user_id__in=admins_id
    ).annotate(
        referrer_pay_id=F('referrer__pay_id')
    ).all()

    if limit:
        users = users[:limit]

    return list(users)


@sync_to_async
def get_paid_users():
    all_users: list[User] = User.objects.exclude(
        Q(is_active=False) | Q(user_id__in=admins_id)
    ).all()

    return list(all_users)


@sync_to_async
def get_user_for_registration(user_id):
    if user_id not in global_users:
        global_users[user_id] = UserData()
    return global_users[user_id]


@sync_to_async
def save_user(
        pay_id,
        user_password,
        user_id,
        user_name,
        phone_number,
        bot_name,
        referrer_id
):
    user = User.objects.create(
        pay_id=pay_id,
        user_password=make_password(user_password),
        is_registered=True,
        is_active=False,
        user_id=user_id,
        invite_link=f"https://t.me/{bot_name}?start={user_id}",
        user_name=user_name,
        phone_number=phone_number,
        referrer_id=referrer_id
    )
    return user


@sync_to_async
def paid_check(user_id) -> bool:
    user = User.objects.filter(user_id=user_id).first()
    if user:
        return user.is_active

    return False


@sync_to_async
def phone_exists(phone_number) -> bool:
    user = User.objects.filter(phone_number=phone_number).first()
    if user:
        return True

    return False


async def send_data_to_admin(admin_chat_id, data_to_send, user_id):
    pay = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Подтвердить',
                    callback_data=PayConfirmCallback(
                        action=PayConfirmAction.CONFIRM,
                        user_id=user_id
                    ).pack()
                ),
                InlineKeyboardButton(
                    text='Отклонить',
                    callback_data=PayConfirmCallback(
                        action=PayConfirmAction.REJECT,
                        user_id=user_id
                    ).pack()
                ),
            ]
        ], resize_keyboard=True, one_time=True
    )
    await bot.send_message(admin_chat_id, data_to_send, reply_markup=pay)


@sync_to_async
def get_user_referral(user_id):
    if user_id not in global_referrals:
        global_referrals[user_id] = ReferralData()
    return global_referrals[user_id]


@sync_to_async
def create_referral(parent_id, referral):
    referral = Referral.objects.create(
        user_id=parent_id,
        referral=referral,
    )
    return referral


@sync_to_async
def create_payment_request(
        user: User
) -> PaymentRequest:
    payment_request = PaymentRequest.objects.update_or_create(
        user_id=user.user_id,
        status=RequestStatus.PROCESSING,
        owner=user
    )

    return payment_request


@sync_to_async
def update_payment_request(
        payment_request: PaymentRequest,
        status: RequestStatus
) -> PaymentRequest:
    payment_request.status = status
    payment_request.save()
    return payment_request


@sync_to_async
def get_user(**kwargs):
    try:
        user = User.objects.get(**kwargs)
        return user
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_payment_status(user_id: int) -> PaymentRequest:
    payment_request = PaymentRequest.objects.filter(
        user_id=user_id
    ).first()

    return payment_request


@sync_to_async
def get_referrals(user_id):
    referrals = User.objects.filter(referrer_id=user_id).all()

    referral_info = [
        {
            'user_id': referral.user_id,
            'pay_id': referral.pay_id,
            'username': referral.user_name,
            'is_active': referral.is_active
        }
        for referral in referrals
    ]
    return referral_info


@sync_to_async
def get_user_for_update(user_id):
    if user_id not in global_update_data:
        global_update_data[user_id] = UserDataUpdatePassword()
    return global_update_data[user_id]


@sync_to_async
def get_user_for_login(user_id):
    if user_id not in global_sign_in:
        global_sign_in[user_id] = UserDataLogin()
    return global_sign_in[user_id]

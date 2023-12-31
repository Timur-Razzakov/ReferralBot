from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password

from bot_ref.models import User

"""Функции для проверки и обновления данных в бд!"""


@sync_to_async
def check_user_chat_id(chat_id):
    return User.objects.filter(user_id=chat_id).exists()


@sync_to_async
def check_user(pay_id):
    return User.objects.filter(pay_id=pay_id).exists()


@sync_to_async
def check_login_chat_id(user_pay_id, chat_id):
    return User.objects.filter(pay_id=user_pay_id, user_id=chat_id).exists()


@sync_to_async
def update_user_is_active(user_id):
    user = User.objects.filter(user_id=user_id).update(is_active=True)
    return user


@sync_to_async
def check_active_user(chat_id):
    """Проверяем оплатил ли пользователь взнос"""
    return User.objects.filter(user_id=chat_id, is_active=True).exists()


@sync_to_async
def update_user_password(pay_id, password):
    user = User.objects.filter(pay_id=pay_id).update(user_password=make_password(password))
    return user

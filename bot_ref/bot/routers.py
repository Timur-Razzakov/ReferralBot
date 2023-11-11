from aiogram import Router, F

from bot_ref.bot.handlers.admin import admin_router
from bot_ref.bot.handlers.authorization import sign_up_router
from bot_ref.bot.handlers.check_paid import check_paid_router
from bot_ref.bot.handlers.default import default_router
from bot_ref.bot.handlers.menu_start_command import commands_router
from bot_ref.bot.handlers.referral import referral_router
from bot_ref.bot.handlers.update_password import update_password_router
from bot_ref.bot.handlers.user_login import sign_in_router
from bot_ref.bot.loader import dp
from bot_ref.bot.middlewares.is_login import IsLoginMiddleware

is_authenticated_routers = Router(name='is_authenticated_routers')
allow_any_routers = Router(name='allow_any_routers')

is_authenticated_routers.include_routers(
    admin_router,
    referral_router,
    check_paid_router,
    default_router
)

is_authenticated_routers.message.filter(F.chat.type == 'private')
is_authenticated_routers.message.middleware(IsLoginMiddleware())
is_authenticated_routers.callback_query.middleware(IsLoginMiddleware())

allow_any_routers.include_routers(
    commands_router,
    update_password_router,
    sign_up_router,
    sign_in_router
)

allow_any_routers.message.filter(F.chat.type == 'private')


dp.include_routers(
    allow_any_routers,
    is_authenticated_routers
)

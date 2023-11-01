import logging

from aiogram import types
from aiogram.types import BotCommand
from django.core.management import BaseCommand

from bot_ref.handlers import default_handlers_register, bot_commands
from bot_ref.handlers.admin import admin_handlers_register
from bot_ref.handlers.authorization import my_router, authorization_handlers_register
from bot_ref.handlers.check_paid import check_paid_handlers_register
from bot_ref.handlers.referral import referral_handlers_register
from bot_ref.handlers.update_password import update_password_handlers_register
from bot_ref.handlers.user_login import login_handlers_register
from bot_ref.keyboards import default_kb
from bot_ref.loader import dp, bot


async def on_startup(_):
    print("Bot has been successfully launched!")


# Запуск бота, обязательно management -> commands -> название -> создание класса Command(BaseCommand)
# my_router = Router(name=__name__) # перенёс в heandler ->authorization.py

class Command(BaseCommand):
    logging.basicConfig(level=logging.DEBUG)

    def handle(self, *args, **options):
        default_handlers_register(dp)
        authorization_handlers_register(dp)
        login_handlers_register(dp)
        update_password_handlers_register(dp)
        referral_handlers_register(dp)
        admin_handlers_register(dp)
        check_paid_handlers_register(dp)

        async def setup_bot_commands():
            commands_for_bot = []
            for cmd in bot_commands:
                commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
            await bot.set_my_commands(commands=commands_for_bot)

        @my_router.message()
        async def unknown_text(message: types.Message):
            await message.answer("Простите, но я не понимаю вас ☹️\n\n"
                                 "Попробуйте использовать команду Помощь ⭐️",
                                 reply_markup=default_kb.only_help_markup)

        dp.run_polling(bot, skip_updates=True, on_startup=on_startup)

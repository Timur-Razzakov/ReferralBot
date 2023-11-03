import logging

from django.core.management import BaseCommand

from bot_ref.bot.loader import bot
from bot_ref.bot.routers import dp


async def on_startup(_):
    print("Bot has been successfully launched!")


class Command(BaseCommand):

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.DEBUG)
        dp.run_polling(bot, skip_updates=True, on_startup=on_startup)

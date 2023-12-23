from aiogram import types, Router, F

from bot_ref.bot.loader import bot
from bot_ref.bot.middlewares.is_paid import IsPaidMiddleware
from bot_ref.bot.texts import default_help_text, support_text

default_router = Router(name=__name__)
default_router.message.middleware(IsPaidMiddleware())


@default_router.message(F.text == 'Помощь ⭐️')
async def cmd_help(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=default_help_text
    )


@default_router.message(F.text == 'Поддержка 🤝')
async def cmd_description(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=support_text
    )

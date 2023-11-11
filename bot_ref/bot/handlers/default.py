from aiogram import types, Router, F

from bot_ref.bot.loader import bot
from bot_ref.bot.middlewares.is_paid import IsPaidMiddleware

HELP_TEXT = """
Привет 👋 я бот который платит Вам за приглашенных друзей! Вы можете использовать такие команды как:

Помощь ⭐️ - помощь по командам бота
Наши контакты 📌 - контакты тех.поддержки и наши соц. сети
Реферальная ссылка 🚀 - получение уникальной реферальной ссылки
Мои рефералы👤 - список приглашенных рефералов с отображением их статусов

Рады что вы используете данного бота ❤️
"""

default_router = Router(name=__name__)
default_router.message.middleware(IsPaidMiddleware())


@default_router.message(F.text == 'Помощь ⭐️')
async def cmd_help(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=HELP_TEXT)


@default_router.message(F.text == 'Поддержка 🤝')
async def cmd_description(message: types.Message):
    support_text = """
    Наши контакты 📌:
Мы в тг: @something
Мы в Ютубе: @something
Мы в инсте: @something

Тех поддержка: @Podderjka
    """
    await bot.send_message(chat_id=message.chat.id,
                           text=support_text)

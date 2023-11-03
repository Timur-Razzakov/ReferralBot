from aiogram import types, Router, F

from bot_ref.bot.keyboards import default_kb
from bot_ref.bot.loader import bot
from bot_ref.bot.middlewares.is_paid import IsPaidMiddleware

HELP_TEXT = """
Привет 👋, я бот по продаже различных товаров! У нас есть такие команды как:

<b>Помощь ⭐️</b> - помощь по командам бота
<b>Описание 📌</> - адрес, контактные данные, график работы
<b>Админ 👑</b> - меню администратора

Но перед началом нужно <b>зарегистрироваться или войти</b> в свой профиль. 
Нажми на команду <b>Регистрация ✌️'</b> или <b>Войти 👋</b>
Если этого не сделаете, некоторые команды будут <b>не доступны</b> 🔴

Рады что вы используете данного бота ❤️
"""

default_router = Router(name=__name__)
default_router.message.middleware(IsPaidMiddleware())


@default_router.message(F.text == 'Помощь ⭐️')
async def cmd_help(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=HELP_TEXT, reply_markup=default_kb.markup)


@default_router.message(F.text == 'Описание 📌')
async def cmd_description(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="Привет ✋, Какой-то текст!!")

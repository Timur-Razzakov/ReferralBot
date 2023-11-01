from aiogram import types, Router, F
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from django.db import router

from bot_ref.handlers.check_data import check_user_chat_id, my_router
from bot_ref.keyboards import sign_inup_kb, default_kb
from bot_ref.loader import bot, dp

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


class ReferralData:
    # храним информацию о реферал пользователя, для сохранения
    def __init__(self):
        self.user_id = None
        self.sender_link_id = None  # id владельца ссылки


referrals = {}


# Создаем функцию для инициализации referrals
@sync_to_async
def get_user_referral(user_id):
    if user_id not in referrals:
        referrals[user_id] = ReferralData()
    return referrals[user_id]


# Сделан дефолтный хендлер
@dp.message(CommandStart())
async def cmd_start(message: types.Message, command: CommandObject, state: FSMContext):
    # await find_user_transaction()
    user_id = message.chat.id
    args = command.args  # получаем id пользователя, владельца ссылки
    if args is not None:
        user_data = await check_user_chat_id(args)
        if user_data:
            if args == str(user_id):
                await message.answer("Вы не можете активировать свой 'invite_code', попробуйте еще раз ↩️")
            else:
                await message.answer("Ура!! Ссылка получена, теперь быстрее регайся!")
                # сохраняем id пользователя для добавления к списку родительских элементов
                referral_data = await get_user_referral(user_id)
                referral_data.user_id = user_id
                referral_data.sender_link_id = args
        else:
            await bot.send_message(chat_id=user_id,
                                   text='Данная ссылка неверна!!!!')
    try:
        await bot.send_message(chat_id=user_id,
                               text=f"Привет ✋ {message.chat.first_name}!\n\n"
                                    f" Для начала <b>нужно зарегистрироваться</b>, "
                                    "иначе остальные команды будут не доступны!\n\n"
                                    "Нажми на команду <b>Регистрация ✌️'</b> или <b>Войти 👋</b>",
                               reply_markup=sign_inup_kb.markup)
    except:
        await message.reply(text="Какой-то текст если ошибка "
                                 "https://t.me/tg")


# @my_router.message(F.text == 'Помощь ⭐️')
async def cmd_help(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=HELP_TEXT, reply_markup=default_kb.markup)


@my_router.message(F.text == 'Описание 📌')
async def cmd_description(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="Привет ✋, Какой-то текст!!")


def default_handlers_register(router: Router) -> None:
    router.message.register(cmd_start, CommandStart())
    router.message.register(cmd_help, F.text == 'Помощь ⭐️')
    router.message.register(cmd_description, F.text == 'Описание 📌')

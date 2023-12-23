from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand

from bot_ref.bot.dataclasses import admins_id
from bot_ref.bot.handlers.check_data import check_user_chat_id
from bot_ref.bot.handlers.user_login import sign_in_text
from bot_ref.bot.keyboards import default_kb, sign_inup_kb, admin_kb
from bot_ref.bot.loader import bot
from bot_ref.bot.utils import check_login, get_user_referral
from config import settings

"""Создаём боковое меню, для выбора команды """
bot_commands = {
    ('start', 'Начала работы с ботом'),
    ('help', 'Помощь и справка', "Информация о командах")
}

commands_router = Router(name=__name__)


@commands_router.message
async def setup_bot_commands(*args, **kwargs):
    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    await bot.set_my_commands(commands=commands_for_bot)


@commands_router.message(CommandStart())
async def cmd_start(message: types.Message, command: CommandObject = None, state: FSMContext = None):
    user_id = message.chat.id
    args = command.args if command.args else settings.MAIN_ADMIN_ID
    # получаем id пользователя, владельца ссылки
    if await check_login(user_id):
        markup = default_kb.markup
        if user_id in admins_id:
            markup = admin_kb.admin_markup

        await message.answer(
            sign_in_text,
            reply_markup=markup
        )
    else:
        if args is not None:
            user_data = await check_user_chat_id(args)
            if user_data:
                if args == str(user_id):
                    await message.answer("Вы не можете активировать свой 'invite_code', попробуйте еще раз ↩️")
                else:
                    await message.answer("Ура!! Ссылка получена, теперь быстрее регистрируйся!")
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
        except Exception:
            await message.reply(text="Какой-то текст если ошибка "
                                     "https://t.me/tg")

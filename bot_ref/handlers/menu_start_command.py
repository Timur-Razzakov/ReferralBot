from aiogram import Router
from aiogram.types import BotCommand

from bot_ref.loader import bot

"""Создаём боковое меню, для выбора команды """
bot_commands = {
    ('start', 'Начала работы с ботом', "..."),
    # ('help', 'Помощь и справка', "Информация о командах")
}


async def setup_bot_commands(*args, **kwargs):
    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    await bot.set_my_commands(commands=commands_for_bot)


def bot_commands_handlers_register(router: Router) -> None:
    router.message.register(setup_bot_commands)

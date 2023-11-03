import random

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from openpyxl.workbook import Workbook
from tabulate import tabulate

from bot_ref.bot.loader import bot
from bot_ref.models import User
from ..dataclasses import admins_id
from ..keyboards import admin_kb, sign_inup_kb
from ..middlewares.is_admin import IsAdminMiddleware
from ..states.roulette_state import RouletteState
from ..utils import check_login, get_users_referrals

HELP_ADMIN_TEXT = '''
Привет администратор 🙋\n\n
На данный момент у тебя есть такие команды как:
--------------------
'''
# получаем список админов

admin_router = Router(name=__name__)
admin_router.message.middleware(IsAdminMiddleware())


@admin_router.message(F.text == 'Рассылка:')
async def send_all(message: types.Message):
    user_id = message.chat.id
    if await check_login(user_id):
        if user_id in admins_id:
            await message.answer(f"Сообщение: <b>{message.text[message.text.find(' '):]}</b> отправляется")
            async for user in User.objects.filter(is_registered=True):
                await bot.send_message(chat_id=user.user_id, text=message.text[message.text.find(' '):])
            await message.answer("Все успешно отправлено!")
        else:
            await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


@admin_router.message(F.text == 'Админ 👑')
async def cmd_admin(message: types.Message):
    user_id = message.chat.id
    if await check_login(user_id):
        if user_id in admins_id:
            await message.answer("Вы вошли в меню администратора 🤴\n\n"
                                 "Ниже предоставлены команды которые вы можете использовать 💭",
                                 reply_markup=admin_kb.markup)
        else:
            await message.answer(
                "Вы не администратор,и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


@admin_router.message(F.text == 'Домой 🏠')
async def cmd_home(message: types.Message):
    user_id = message.chat.id
    if await check_login(user_id):
        if user_id in admins_id:
            await message.answer(
                "Вы успешно перешли в главное меню!",
                reply_markup=admin_kb.admin_markup
            )
        else:
            await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


@admin_router.message(F.text == 'Помощь 🔔')
async def cmd_help_admin(message: types.Message):
    user_id = message.chat.id
    if await check_login(user_id):
        if user_id in admins_id:
            await message.answer(text=HELP_ADMIN_TEXT, reply_markup=admin_kb.markup)
        else:
            await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


@admin_router.message(F.text == 'Краткая статистика 📈')
async def short_statistics(message: types.Message):
    all_users: list[User] = await get_users_referrals(0)

    # Добавим информацию о рефералах для каждого пользователя
    data_with_referrals = [
        [user.pk, user.user_name, user.binance_id]
        for user in all_users
    ]

    # Заголовки столбцов
    headers = ["id", "name", "binance_id"]

    # Форматирование и вывод таблицы
    table = tabulate(data_with_referrals, headers, tablefmt="pretty")

    html = f'<pre>{table}</pre>'

    await message.answer(html, parse_mode='HTML')


@admin_router.message(F.text == 'Полная статистика 📊')
async def full_statistics(message: types.Message):
    all_users: list[User] = await get_users_referrals(0)

    # Добавим информацию о рефералах для каждого пользователя
    data_with_referrals = [
        [
            user.pk,
            user.user_name,
            user.binance_id,
            user.referrer_id,
            user.phone_number,
            '✅ Yes' if user.is_active else '❌ No'
        ]
        for user in all_users
    ]

    # Заголовки столбцов
    headers = [
        'id',
        'name',
        'binance id',
        'referrer id',
        'phone number',
        'paid status'
    ]

    # Форматирование и вывод таблицы
    table = tabulate(data_with_referrals, headers, tablefmt="pretty")
    html = f'<pre>{table}</pre>'

    await message.answer(html, parse_mode='HTML')


@admin_router.message(F.text == 'Выгрузить в excel ⬇️')
async def download_as_execl(message: types.Message):
    users = await get_users_referrals(0)

    wb = Workbook()
    sh1 = wb.active
    sh1.title = 'Report'

    sh1.append(
        (
            'id',
            'name',
            'binance id',
            'referrer id',
            'phone number',
            'paid status'
        )
    )

    for user in users:
        sh1.append(
            (
                user.pk,
                user.user_name,
                user.binance_id,
                user.referrer_id,
                user.phone_number,
                '✅ Yes' if user.is_active else '❌ No'
            )
        )

    wb.save('./bot_ref/bot/reports/report.xlsx')

    file = FSInputFile('./bot_ref/bot/reports/report.xlsx')
    await message.answer_document(file)


@admin_router.message(F.text == 'Рулетка 🎲')
async def roulette(message: types.Message, state: FSMContext):
    await message.answer('Выберите число участников')
    await state.set_state(RouletteState.limit)


@admin_router.message(RouletteState.limit)
async def start_roulette(message: types.Message, state: FSMContext):
    limit = int(message.text)
    all_users: list[User] = await get_users_referrals(0)

    part_users = random.sample(all_users, min(limit, len(all_users)))

    # Добавим информацию о рефералах для каждого пользователя
    data_with_referrals = [
        [user.pk, user.user_name, user.binance_id]
        for user in part_users
    ]

    # Заголовки столбцов
    headers = ["id", "name", "binance_id"]

    # Форматирование и вывод таблицы
    table = tabulate(data_with_referrals, headers, tablefmt="pretty")
    html = f'<pre>{table}</pre>'
    await state.clear()

    await message.answer(html, parse_mode='HTML')

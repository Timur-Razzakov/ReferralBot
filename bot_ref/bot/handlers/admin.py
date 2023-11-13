import random

from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from openpyxl.workbook import Workbook
from tabulate import tabulate

from bot_ref.bot.loader import bot
from bot_ref.models import User
from ..keyboards import admin_kb
from ..middlewares.is_admin import IsAdminMiddleware
from ..states.mailing_state import MailingState
from ..states.roulette_state import RouletteState
from ..utils import get_users_referrals, get_paid_users

HELP_ADMIN_TEXT = '''
Привет администратор 🙋 У вас есть такие команды как:

Домой 🏠 - вернет Вас в меню пользователя
Помощь 🔔 - помощь по командам бота
Рулетка 🎲 - выбор N случайных, авторизированных пользователей.
После нажатия Рулетки, нужно будет ввести количество пользователей которое Вы хотите получить, это должно быть целое число (Например: 1, 2, 3), после отправки числа сразу будут присланы ID, Имя и PayID счастливчиков!
Краткая статистика 📈 - выводит неполные данные пользователей (ID, Имя, PayID)
Полная статистика 📊 - вывод все данные о пользователях (ID, Имя, PayID, ID рефовода, номер, статус)
Выгрузить в excel ⬇️ - получение Excel файла с полной статистикой пользователей
'''

admin_router = Router(name=__name__)
admin_router.message.middleware(IsAdminMiddleware())


async def send_mailing(message: types.Message):
    users = await get_paid_users()
    text = message.text[message.text.find(':') + 1:]
    await message.answer('Сообщение: отправляется')

    for user in users:
        try:
            await bot.send_message(chat_id=user.user_id, text=text)
        except TelegramBadRequest:
            print('error', user.user_id, user.user_name)

    await message.answer('Все успешно отправлено!')


@admin_router.message(F.text.regexp('Рассылка:'))
async def send_all(message: types.Message):
    await send_mailing(message)


@admin_router.message(F.text == 'Рассылка 📧')
async def send_mailing_start(message: types.Message, state: FSMContext):
    await message.answer('Введите текст рассылки 📧')
    await state.set_state(MailingState.status)


@admin_router.message(MailingState.status)
async def mailing_send(message: types.Message, state: FSMContext):
    await send_mailing(message)
    await state.clear()


@admin_router.message(F.text == 'Админ 👑')
async def cmd_admin(message: types.Message):
    await message.answer('Вы вошли в меню администратора 🤴\n\n'
                         'Ниже предоставлены команды которые вы можете использовать 💭',
                         reply_markup=admin_kb.markup)


@admin_router.message(F.text == 'Домой 🏠')
async def cmd_home(message: types.Message):
    await message.answer(
        'Вы успешно перешли в главное меню!',
        reply_markup=admin_kb.admin_markup
    )


@admin_router.message(F.text == 'Помощь 🔔')
async def cmd_help_admin(message: types.Message):
    await message.answer(text=HELP_ADMIN_TEXT)


@admin_router.message(F.text == 'Краткая статистика 📈')
async def short_statistics(message: types.Message):
    all_users: list[User] = await get_users_referrals(0)

    # Добавим информацию о рефералах для каждого пользователя
    data_with_referrals = [
        [user.pk, user.user_name, user.pay_id]
        for user in all_users
    ]

    # Заголовки столбцов
    headers = ['id', 'name', 'pay_id']

    # Форматирование и вывод таблицы
    table = tabulate(data_with_referrals, headers, tablefmt='pretty')

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
            user.pay_id,
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
        'pay id',
        'referrer id',
        'phone number',
        'paid status'
    ]

    # Форматирование и вывод таблицы
    table = tabulate(data_with_referrals, headers, tablefmt='pretty')
    html = (f'На данный момент у Вас {len(all_users)} рефералов:'
            f'<pre>{table}</pre>')

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
            'pay id',
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
                user.pay_id,
                user.referrer_pay_id,
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
    if not message.text.isdigit():
        await message.answer('Рулетка принимает только число ‼️')
        return

    limit = int(message.text)
    all_users: list[User] = await get_paid_users()

    part_users = random.sample(all_users, min(limit, len(all_users)))

    # Добавим информацию о рефералах для каждого пользователя
    data_with_referrals = [
        [user.pk, user.user_name, user.pay_id]
        for user in part_users
    ]

    # Заголовки столбцов
    headers = ['id', 'name', 'pay_id']

    # Форматирование и вывод таблицы
    table = tabulate(data_with_referrals, headers, tablefmt='pretty')
    html = f'<pre>{table}</pre>'
    await state.clear()

    await message.answer(html, parse_mode='HTML')

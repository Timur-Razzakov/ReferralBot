from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from tabulate import tabulate

from bot_ref.keyboards import sign_inup_kb, admin_kb, default_kb
from bot_ref.loader import bot, dp
from bot_ref.models import User
from config import settings as config
from .authorization import my_router
from .referral import get_referrals, get_data, get_user, get_users_sync
from .user_login import get_user_for_login

HELP_ADMIN_TEXT = '''
Привет администратор 🙋\n\n
На данный момент у тебя есть такие команды как:
--------------------
'''
# получаем список админов
admins_id = [int(id) for id in config.ADMINS.split(',') if id]


async def check_login(user_id):
    # Проверяем авторизовался ли пользователь или нет
    user = await get_user_for_login(user_id)
    if user.current_state:
        return True
    else:
        return False


@my_router.message(F.text == 'Рассылка:')
async def send_all(message: types.Message):
    user_id = message.chat.id
    if await check_login(user_id):
        if user_id in admins_id:
            await message.answer(f"Сообщение: <b>{message.text[message.text.find(' '):]}</b> отправляется")
            async for user in User.objects.filter(is_registered=True):
                await bot.send_message(chat_id=user.chat_id, text=message.text[message.text.find(' '):])
            await message.answer("Все успешно отправлено!")
        else:
            await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


@my_router.message(F.text == 'Админ 👑')
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


@my_router.message(F.text == 'Домой 🏠')
async def cmd_home(message: types.Message):
    user_id = message.chat.id
    if await check_login(user_id):
        if user_id in admins_id:
            await message.answer("Вы успешно перешли в главное меню!", reply_markup=default_kb.markup)
        else:
            await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


@my_router.message(F.text == 'Помощь 🔔')
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


@my_router.message(F.text == 'Статистика')
async def get_statistika(message: types.Message):
    # user_id = message.chat.id
    # if await check_login(user_id):
    #     if user_id in admins_id:
    all_users = await get_all_users_with_referrals()
    # print(all_users)
    for user_id, data in all_users.items():
        print(user_id)
        print('---------------------------------------')
        print(data)
    data = [
        [1, "John", "2023-10-27", 1001, 50],
        [2, "Alice", "2023-10-27", 1002, 0],
        [3, "Bob", "2023-10-27", 1003, 25],
        [4, "Eve", "2023-10-28", 1004, 0],
        [1, "John", "2023-10-27", 1005, 75],
    ]

    # Добавим информацию о рефералах для каждого пользователя
    data_with_referrals = [
        [user, name, date, id, payment]
        for user, name, date, id, payment in data
    ]

    # Заголовки столбцов
    headers = ["user", "name", "date", "id", "payment"]

    # Форматирование и вывод таблицы
    table = tabulate(data_with_referrals, headers, tablefmt="fancy_grid")
    await message.answer(table)
    # message_text = "<b>Информация о рефералах:</b>\n"
    # for user_id, data in all_users.items():
    #     user_info = data['user_info']
    #     referrals = data['referrals']
    #
    #     message_text += "<pre>"
    #     message_text += "{:<15} {:<15} {:<15} {:<10}\n".format("User ID", "Username", "Pay ID",
    #                                                            "Paid")
    #     message_text += "{:<15} \n".format(user_info.user_id)
    #     message_text += "</pre>\n"
    #
    #     if referrals:
    #         message_text += "<pre>"
    #         message_text += "{:<15} {:<15} {:<15} {:<10}\n".format("Referral ID", "Username", "Pay ID",
    #                                                                "Paid")
    #         # Добавьте данные рефералов (если они есть)
    #         for referral in referrals:
    #             message_text += "{:<15} {:<15} {:<15} {:<10}\n".format(referral['user_id'],
    #                                                                    referral['username'],
    #                                                                    referral['binance_id'],
    #                                                                    '✅ Yes' if referral[
    #                                                                        'is_active'] else '❌ No')
    #         message_text += "</pre>"
    # await message.answer(table)
    #     else:
    #         await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    # else:
    #     await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
    #                          reply_markup=sign_inup_kb.markup)


async def get_all_users_with_referrals():
    all_users = {}
    # получаем всех пользователей
    users = await get_users_sync()
    for user in users:
        # получаем рефералов для каждого пользователя
        user_referrals = await get_referrals(user['pk'])
        all_users[user['user_id']] = {
            'user_info': user,
            'referrals': user_referrals
        }
    return all_users


def admin_handlers_register(router: Router) -> None:
    router.message.register(cmd_admin, F.text == 'Админ 👑')
    router.message.register(send_all, F.text == 'Рассылка:')
    router.message.register(get_statistika, F.text == 'Статистика')
    router.message.register(cmd_home, F.text == 'Домой 🏠')
    router.message.register(cmd_help_admin, F.text == 'Помощь 🔔')
    # router.message.register(get_static, F.text == 'Помощь 🔔')

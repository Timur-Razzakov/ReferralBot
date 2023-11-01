from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from tabulate import tabulate

from bot_ref.keyboards import sign_inup_kb, admin_kb, default_kb, paid_ikb
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
    user_id = message.chat.id
    # if await check_login(user_id):
    #     if user_id in admins_id:
    all_users = await get_all_users_with_referrals()
    for key in all_users.keys():
        user_info = all_users[key]['user_info']
        info_string = f"🆔 {user_info['pk']}\n Username: {user_info['username']}\n Binance ID: {user_info['binance_id']}\n Is active: {user_info['is_active']}\n Payment count: {user_info['count_payment']}\n\nReferrals:\n"
        if len(all_users[key]['referrals']) == 0:
            info_string += "No Referrals\n\n"
        else:
            for i in range(len(all_users[key]['referrals'])):
                ref = all_users[key]['referrals'][i]
                info_string += f"\n🔗 Referral {i + 1}:\n Username: {ref['username']}\n Binance ID: {ref['binance_id']}\n Is active: {ref['is_active']}\n\n"
        await bot.send_message(user_id, info_string, parse_mode='Markdown', reply_markup=None)

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

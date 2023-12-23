# !!!!!! ВАЖНО !!!!!!
# НЕ УДАЛЯТЬ ТРОЙНЫЕ КОВЫЧКИ """..."""
# В НАЧАЛЕ И КОНЦЕ ТЕКСТОВ.

# Примечание символы \n в текстах используются
# для переноса строки (enter) между строками.


#############################
# ADMIN TEXTS
#############################

admin_hello_text = """
Вы вошли в меню администратора 🤴\n\n
Ниже предоставлены команды которые вы можете использовать 💭
"""

admin_help_text = """
Привет администратор 🙋 У вас есть такие команды как:

Домой 🏠 - вернет Вас в меню пользователя
Помощь 🔔 - помощь по командам бота
Рулетка 🎲 - выбор N случайных, авторизированных пользователей.
После нажатия Рулетки, нужно будет ввести количество пользователей которое Вы хотите получить, это должно быть целое число (Например: 1, 2, 3), после отправки числа сразу будут присланы ID, Имя и PayID счастливчиков!
Краткая статистика 📈 - выводит неполные данные пользователей (ID, Имя, PayID)
Полная статистика 📊 - вывод все данные о пользователях (ID, Имя, PayID, ID рефовода, номер, статус)
Выгрузить в excel ⬇️ - получение Excel файла с полной статистикой пользователей
"""

home_menu_text = """
Вы успешно перешли в главное меню!
"""

# Сообщение выводится при использовании рулетки.

roulette_member_text = """
Выберите число участников
"""

roulette_member_error_text = """
Рулетка принимает только число ‼️
"""

# Сообщение выводится при отправке рассылок.
mailing_text = """
Введите текст рассылки 📧
"""

mailing_send_text = """
Сообщение: отправляется
"""

mailing_send_success_text = """
Все успешно отправлено!
"""

#############################
# REGISTRATIONS TEXTS
#############################

registration_text = """
Для регистрации сначала напишите свой Binance Pay_Id!
❔Подробную информацию о том что из себя представляет Pay_Id и где его искать вы найдете на официальном сайте Binance: 
https://www.binance.com/ru/support/faq/%D0%BA%D0%B0%D0%BA-%D0%BD%D0%B0%D0%B9%D1%82%D0%B8-binance-pay-id-f3040335259a4b1ea68934daf94bab1d

‼️Перед тем как отравить Ваш Pay_Id убедитесь что вы написали его правильно!
"""

registration_success_text = """
Регистрация прошла успешно ✅ \n\n
Теперь Вам нужно зайти в свой аккаунт
 с помощью команды Войти 👋
"""

cancel_action_text = """
Операция успешно отменена 🙅‍
"""

user_id_error_text = """
Пользователь с таким ID как у вас уже есть, войдите в свой аккаунт 🫡
"""

# <b> </b> делать текст внутри него жирным
pay_id_error_text = """
Пользователь с таким pay_id <b>уже есть</b>, попробуйте еще раз ↩️
"""

pay_id_type_error_text = """
Pay_id должен состоять только из <b>цифр 🔢</b>\n\n
Попробуйте еще раз ↩️!
"""

user_name_text = """
Теперь напиши ваше имя ✍️
"""

phone_number_text = """
Следующий шаг: отправьте номер Вашего телефона✍️

Важно знать❗️

Мы не пишем, не звоним и храним ваши данные пользователя в конфиденциальности!🔐

Убедительная просьба‼️

Убедитесь, что вы ввели свой рабочий номер телефона! В случае утери пользовательского пароля, восстановление будет возможным только через номер телефона!
Формат номера телефона должно быть полным!📝

Пример: +71234567890  ✅
"""

password_text = """
Теперь придумайте и напишите пароль ✍️
"""

retry_password_text = """
Введи пароль <b>еще раз</b> 🔄
"""

password_error_text = """
Вы ввели пароль <b>не правильно</b> ❌\n\n
Попробуйте еще раз 🔄
"""

password_letters_error_text = """
Пароль должен быть только из <b>латинских букв</b> 
и содержать хотя бы <b>одну цифру</b>\n\n
Повторите попытку 🔄
"""

# {user_name} - не удалять иначе бот сломается,
# туда будут подставляться имена пользователей

new_referral_text = """
У вас появился реферал по имени: {user_name}
"""

# {} - ки и то что внутри них не удалять

new_referral_notification_text = """
Пользователь {referrer_user_name} пригласил 
пользователя {referral_user_name} и заработал 100 USDT
"""

#############################
# LOGIN TEXTS
#############################

sign_in_text = """
Вход был успешно выполнен ⭐️
"""

payment_text = """
Запрос на оплату
LiveMoney_admin отправил(а) запрос на оплату на сумму 100 USDT. Нажмите на эту ссылку, чтобы оплатить.
Pay id для оплаты: 730533334 
Ссылка: https://s.binance.com/GjAhZbFe
"""

help_text = """
Хотите узнать, как начать зарабатывать с нашим ботом? Вот шаги для регистрации:

Нажмите Регистрация ✌️ и введите ваш Binance Pay ID, имя и номер телефона.
Создайте пароль и подтвердите его, чтобы обеспечить безопасность вашего аккаунта.
После регистрации, используйте Войти👋 и начните свой путь к заработку!
Функционал бота включает в себя приглашение рефералов и вознаграждение за каждого приглашенного. Следите за вашим балансом и собирайте награды!

Если у вас возникли какие-либо вопросы или вам нужна дополнительная помощь, не стесняйтесь обращаться к нам @Podderlka. Мы всегда готовы помочь!
"""

input_pay_id_text = """
Введите свой Pay_Id ✨
"""

input_password_text = """
Теперь вам нужно ввести пароль 🔐
"""

login_error_text = """
Такого логина <b>нет</b>, повторите еще раз ❌
"""

input_password_error_text = """
Пароль <b>не правильный</b> попробуйте еще раз 🔄
"""

#############################
# RESET PASSWORD TEXTS
#############################

reset_password_pay_id_text = """
Чтобы изменить пароль, для начала введите ваш Pay_Id 🫡
"""

new_password_text = """
Pay_Id <b>успешно</b> найден,
и ID пользователя совпадает с логином 🌟\n\n 
Теперь вы <b>сможете</b> изменить пароль ✅\n\n
Введите <b>новый пароль</b> ✍️
"""

new_password_error_text = """
Пароль должен быть только из <b>латинских букв</b> 
и содержать хотя бы <b>одну цифру</b>\n\n
Повторите попытку 🔄
"""

repeat_new_password_text = """
Введи пароль <b>еще раз</b> 🔄
"""

password_input_error_text = """
Вы ввели пароль <b>не правильно</b> ❌\n\n
Попробуйте еще раз 🔄
"""

reset_password_error_text = """
Вы <b>не прошли проверку</b> ❌\n\n
На это могут быть две причины:\n
1. Такого логина нет\n
2. Ваш ID пользователя не совпадает с Pay_Id который вы указали\n\n
Вы можете <b>повторить</b> попытку 🔄
"""

success_password_change_text = """
Изменение пароля прошла <b>успешно</b> ✅\n\n
Теперь, войдите в свой профиль 💝
"""

#############################
# PAYMENT TEXTS
#############################

paid_text = """
❗️Прежде чем пользоваться функционалом бота и начать зарабатывать приглашая друзей, Вам необходимо внести единоразовый взнос в размере 100$
После оплаты пожалуйста нажмите кнопку Оплатил 🤑
"""

success_payment_text = """
Вы уже оплатили взнос 🥳
"""

# {status} - не удалять
repeated_payment_request_text = """
Вы уже отправляли заявку на проверку оплаты
ниже вы можете узнать его статус\n\n
Статус заявки: {status}
"""

payment_help_text = """
<b>Заметка:</b>\n
После совершения оплаты, вы должны нажать на эту кнопку. После проверки, 
мы активируем ваш аккаунт!
"""

payment_data_sent_admin_text = """
Данные отправлены админу 📨 \n\n
Пожалуйста ожидайте верификации аккаунта!
"""

payment_reject_text = """
Ваша Заявка отклонена🙅

❗️Если у Вас возникли какие-то проблемы или вопросы, обращайтесь в нашу поддержку @Poderjka
"""

payment_confirm_text = """
✅Ваша заявка подтверждена, добро пожаловать!

Скорее начинайте зарабатывать с нами!
"""

#############################
# DEFAULT TEXTS
#############################

default_help_text = """
Привет 👋 я бот который платит Вам за приглашенных друзей! Вы можете использовать такие команды как:

Помощь ⭐️ - помощь по командам бота
Наши контакты 📌 - контакты тех.поддержки и наши соц. сети
Реферальная ссылка 🚀 - получение уникальной реферальной ссылки
Мои рефералы👤 - список приглашенных рефералов с отображением их статусов

Рады что вы используете данного бота ❤️
"""

support_text = """
Наши контакты 📌:
Мы в тг: @something
Мы в Ютубе: @something
Мы в инсте: @something

Тех поддержка: @Podderjka
"""

#############################
# REFERRAL TEXTS
#############################

login_required_text = """
С начало авторизуйтесь 🤚
"""

# {invite_link} - не удалять
referral_text = """
Ваша реферальная ссылка: {invite_link}

‼️Убедитесь что реферал регистрируется в боте по вашей ссылке!
❌Иначе платеж за реферала не будет одобрен❌
"""

not_paid_referral_text = """
Сначала совершите взнос в размере 100$
"""

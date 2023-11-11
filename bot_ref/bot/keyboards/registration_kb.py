from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Реализована клавиатура команды отмена
markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Отмена ❌", callback_data='all_users'),

    ],
],
    resize_keyboard=True, one_time_keyboard=True)


# Реализована клавиатура команды забыли пароль
markup_cancel_forgot_password = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Отмена ❌", callback_data='all_users'),
        KeyboardButton(text='Забыли пароль? 🆘')

    ],
],
    resize_keyboard=True,
    one_time_keyboard=True)

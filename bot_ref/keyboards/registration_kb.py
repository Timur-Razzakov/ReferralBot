from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Реализована клавиатура команды отмена
markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=" Отмена ❌"),

    ],
],
    resize_keyboard=True, one_time_keyboard=True)

# Реализована клавиатура команды Забыли пароль
markup_cancel_forgot_password = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=" Отмена ❌"),
        KeyboardButton(text='Забыли пароль? 🆘')

    ],
],
    resize_keyboard=True,
    one_time_keyboard=True,)

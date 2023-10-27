from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Реализована дефолтная клавиатура
markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Помощь ⭐️'),
            KeyboardButton(text='Описание 📌'),
            KeyboardButton(text='Админ 👑')
        ],
        [
            KeyboardButton(text='Реферальная ссылка 🚀'),
            KeyboardButton(text='Мои рефералы ')
        ],
        [
            KeyboardButton(text='Оплатил 🤑'),
        ]
    ],
    resize_keyboard=True)

# Реализована клавиатура команды Помощь
only_help_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Помощь ⭐️'),

        ],
    ],
    resize_keyboard=True, one_time_keyboard=True)
#

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Помощь ⭐️'),
            KeyboardButton(text='Описание 📌'),
        ],
        [
            KeyboardButton(text='Реферальная ссылка 🚀'),
            KeyboardButton(text='Мои рефералы ')
        ],
    ],
    resize_keyboard=True
)

paid_kb = ReplyKeyboardMarkup(
    keyboard=[
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

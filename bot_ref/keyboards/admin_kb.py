from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Реализована клавиатура админа
markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Домой 🏠"),
            KeyboardButton(text="Помощь 🔔"),
            KeyboardButton(text="Статистика"),
        ],
    ],
    resize_keyboard=True, one_time_keyboard=True)

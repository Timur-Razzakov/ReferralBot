from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Регистрация ✌️"),
            KeyboardButton(text="Войти 👋"),
            KeyboardButton(text="Помощь 🆘"),
        ],
    ],
    resize_keyboard=True)


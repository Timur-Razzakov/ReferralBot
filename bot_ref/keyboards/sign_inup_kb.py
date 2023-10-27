from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=" Регистрация ✌️"),
            KeyboardButton(text="Войти 👋"),
            KeyboardButton(text=" Забыли пароль? 🆘"),
        ],
    ],
    resize_keyboard=True)


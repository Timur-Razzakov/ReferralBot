from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Реализована клавиатура админа
markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Домой 🏠"),
            KeyboardButton(text="Помощь 🔔"),
            KeyboardButton(text="Рулетка 🎲")
        ],
        [
            KeyboardButton(text="Краткая статистика 📈"),
            KeyboardButton(text="Полная статистика 📊"),
        ],
        [
            KeyboardButton(text="Выгрузить в excel ⬇️"),
        ],
    ],
    resize_keyboard=True, one_time_keyboard=True)

admin_markup = ReplyKeyboardMarkup(
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
    ],
    resize_keyboard=True
)

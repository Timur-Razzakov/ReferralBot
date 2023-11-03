from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_paid = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отправить на проверку', callback_data="send", one_time=True)
        ]
    ], resize_keyboard=True,
)

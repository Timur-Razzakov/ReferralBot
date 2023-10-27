from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_paid = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отправить на проверку', callback_data="send",one_time=True )
        ]
    ], resize_keyboard=True,
)

pay = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подтвердить', callback_data="confirm"),
            InlineKeyboardButton(text='Отклонить', callback_data="reject" ),
        ]
    ], resize_keyboard=True,one_time=True
)

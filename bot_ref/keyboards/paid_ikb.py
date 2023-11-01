from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_paid = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отправить на проверку', callback_data="send")
        ]
    ], resize_keyboard=True, one_time=True
)

pay = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подтвердить', callback_data="confirm"),
            InlineKeyboardButton(text='Отклонить', callback_data="reject"),
        ]
    ], resize_keyboard=True, one_time=True
)
send_money = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Оплатил', callback_data="payment"),
        ]
    ], resize_keyboard=True, one_time=True
)

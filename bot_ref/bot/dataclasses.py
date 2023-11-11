import enum

from aiogram.filters.callback_data import CallbackData

from config import settings as config

admins_id = [
    int(admin_id) for admin_id in config.ADMINS.split(',') if admin_id
]


class UserData:
    def __init__(self):
        self.user_id = None
        self.pay_id = None
        self.user_name = None
        self.phone_number = None
        self.invite_link = None
        self.user_password = None
        self.repeat_password = None
        self.bot_name = None


global_users = {}


class ReferralData:
    # храним информацию о реферал пользователя, для сохранения
    def __init__(self):
        self.user_id = None
        self.sender_link_id = None  # id владельца ссылки


global_referrals = {}


class UserDataUpdatePassword:
    def __init__(self):
        self.user_id = None
        self.pay_id = None
        self.new_password = None
        self.repeat_password = None


global_update_data = {}


class UserDataLogin:
    def __init__(self):
        self.user_id = None
        self.pay_id = None
        self.password = None
        self.current_state = False


a = UserDataLogin()
a.current_state = True
a.user_id = 1457037393
a.pay_id = 1111


b = UserDataLogin()
b.current_state = False
b.user_id = 818429523
b.pay_id = 2222
global_sign_in = {1457037393: a, 818429523: b}


class PayConfirmAction(enum.Enum):
    CONFIRM = 'CONFIRM'
    REJECT = 'REJECT'


class PayConfirmCallback(CallbackData, prefix='pay_confirm'):
    action: PayConfirmAction
    user_id: int | str = None

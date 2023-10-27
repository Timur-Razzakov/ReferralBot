from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode

from config import settings as config

# Создаем нашего бота и диспатчер, MemoryStorage хранилище состояний
bot = Bot(token=config.TOKEN_API, parse_mode=ParseMode.HTML,)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

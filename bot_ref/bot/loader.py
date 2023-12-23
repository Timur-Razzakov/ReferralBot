from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings as config

# Создаем нашего бота и диспетчера, MemoryStorage хранилище состояний
bot = Bot(token=config.TOKEN_API, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

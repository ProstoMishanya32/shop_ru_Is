# - *- coding: utf- 8 - *-
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from modules.utils import main_config



bot = Bot(token=main_config.bot.token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


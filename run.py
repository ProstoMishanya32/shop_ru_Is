# - *- coding: utf- 8 - *-
import os, sys, colorama
from modules.utils.logging_system import logger
from aiogram import executor, Dispatcher
from handlers import dp
from modules.utils import main_config
from modules import alerts
from modules.services import db

colorama.init()

# запуск бота

async def on_startup(dp: Dispatcher):
    await alerts.on_startup_notify(dp)
    db.start_bot(colorama)
    logger.warning("Бот вошел в сеть")
    print(colorama.Fore.LIGHTBLUE_EX + "--- Бот вошел в сеть ---\n" + colorama.Fore.LIGHTRED_EX +
    "--- Разработчик @michailcoding ---\n"
    + colorama.Fore.YELLOW + "--- https://kwork.ru/user/prostomishanya32 ---" +  colorama.Fore.RESET)







if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)

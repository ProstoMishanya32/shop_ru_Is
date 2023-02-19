# - *- coding: utf- 8 - *-
from aiogram import Dispatcher
from modules.utils import main_config, ded, real_time
from bot_telegram import bot




# Уведомление и проверка обновления при запуске бота
async def on_startup_notify(dp: Dispatcher):
    await send_admins(ded(f"""
                      <b>❗️Бот вошел в сеть ️️.  {real_time}</b>
                      ➖➖➖➖➖➖➖➖➖➖➖➖
                      <code>Данное сообщение видят только администаторы бота.</code>
                      ➖➖➖➖➖➖➖➖➖➖➖➖
                      В случае каких-то проблем, обращаться @michailcoding
                      """))


# Рассылка сообщения всем администраторам
async def send_admins(message, markup=None, not_me=0):
    await bot.send_message(main_config.bot.main_admin, message, reply_markup=markup, disable_web_page_preview=True)

    for admin in main_config.bot.admins:
        try:
            if str(admin['user_id']) != str(not_me):
                await bot.send_message(admin['user_id'], message, reply_markup=markup, disable_web_page_preview=True)
        except Exception as i:
           print(i)


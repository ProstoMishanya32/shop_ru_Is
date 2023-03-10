# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup
from modules.services import db, json_logic
from modules.utils import main_config

# Кнопки главного меню
def menu(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    check  = db.check_user(user_id)
    if check == "il":
        keyboard.row("🏠 הערוץ שלנו","🎁 קטלוג", "☎ תמיכה")
        keyboard.row("🇮🇱 שנה שפה 🇷🇺")
        if user_id in json_logic.get_admins() or user_id == main_config.bot.main_admin:
            keyboard.add('🎁 ניהול מוצר', '⚒ ערוך טקסט', '🛎 ניוזלטר')
            keyboard.add('💲 קביעת הנחה', '❌ הסר הנחה')
        if user_id == main_config.bot.main_admin:
            keyboard.add("🧑‍✈️ מנהלים")
    else:
        keyboard.row("🏠 Наш канал","🎁 Каталог", "☎ Поддержка")
        keyboard.row("🇮🇱 Сменить язык 🇷🇺")
        if user_id in json_logic.get_admins() or user_id == main_config.bot.main_admin:
            keyboard.add('🎁 Управление товарами','⚒ Редактировать текста','🛎 Рассылка')
            keyboard.add('💲 Установление скидки', '❌ Удаление скидки')
        if user_id == main_config.bot.main_admin:
            keyboard.add("🧑‍✈️ Администаторы")
    return keyboard

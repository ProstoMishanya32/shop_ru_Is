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
        keyboard.row("🛒 עגלת קניות", "📪 Мои заказы")
        keyboard.row("🇮🇱 שנה שפה 🇷🇺")
        if user_id in json_logic.get_admins() or user_id == main_config.bot.main_admin:
            keyboard.add('🎁 ניהול סחורה', '🕐 היסטוריית הזמנות', 'קביעת הנחה 💲')
        if user_id == main_config.bot.main_admin:
            keyboard.add("🧑‍✈️ מנהלים")
    else:
        keyboard.row("🏠 Наш канал","🎁 Каталог", "☎ Поддержка")
        keyboard.row("🛒 Корзина", "📪 Мои заказы")
        keyboard.row("🇮🇱 Сменить язык 🇷🇺")
        if user_id in json_logic.get_admins() or user_id == main_config.bot.main_admin:
            keyboard.add('🎁 Управление товарами', '🕐 История заказов', 'Установление скидки 💲')
        if user_id == main_config.bot.main_admin:
            keyboard.add("🧑‍✈️ Администаторы")
    return keyboard

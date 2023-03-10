# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton






def select_lang():
    keyboard = InlineKeyboardMarkup(
    ).add(InlineKeyboardButton("🇷🇺 Русский", callback_data="select_lang:ru")
    ).add(InlineKeyboardButton("🇮🇱 עִברִית", callback_data= "select_lang:il"))
    return keyboard

def item_open(item_id, category_id, remover, check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup(
        ).add(
            InlineKeyboardButton("💰 Купить товар", callback_data=f"buy_item_open_finl:{item_id}:{remover}")
        ).add(
            InlineKeyboardButton("⬅ Вернуться ↩", callback_data=f"buy_category_open:{category_id}:{remover}")
        )
    else:
        keyboard = InlineKeyboardMarkup(
        ).add(
            InlineKeyboardButton("להזמין", callback_data=f"buy_item_open_finl:{item_id}:{remover}")
        ).add(
            InlineKeyboardButton("⬅ חזרה ↩", callback_data=f"buy_category_open:{category_id}:{remover}")
        )

    return keyboard

def get_discount(item_id, category_id, remover, check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("⬅ Вернуться ↩", callback_data=f"buy_category_open_discout:{category_id}:{remover}"))
    else:
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("⬅ חזרה ↩", callback_data=f"buy_category_open_discout:{category_id}:{remover}"))
    return keyboard

def buy_item(check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("✅", callback_data=f"buy_item_final:yes")).insert(
            InlineKeyboardButton("❌", callback_data=f"buy_item_final:no"))
    else:
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("❌", callback_data=f"buy_item_final:yes")).insert(
            InlineKeyboardButton("✅", callback_data=f"buy_item_final:no"))
    return keyboard
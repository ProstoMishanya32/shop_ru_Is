# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton






def select_lang():
    keyboard = InlineKeyboardMarkup(
    ).add(InlineKeyboardButton("๐ท๐บ ะ ัััะบะธะน", callback_data="select_lang:ru")
    ).add(InlineKeyboardButton("๐ฎ๐ฑ ืขึดืืจึดืืช", callback_data= "select_lang:il"))
    return keyboard

def item_open(item_id, category_id, remover, check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup(
        ).add(
            InlineKeyboardButton("๐ฐ ะัะฟะธัั ัะพะฒะฐั", callback_data=f"buy_item_open_finl:{item_id}:{remover}")
        ).add(
            InlineKeyboardButton("โฌ ะะตัะฝััััั โฉ", callback_data=f"buy_category_open:{category_id}:{remover}")
        )
    else:
        keyboard = InlineKeyboardMarkup(
        ).add(
            InlineKeyboardButton("ืืืืืื", callback_data=f"buy_item_open_finl:{item_id}:{remover}")
        ).add(
            InlineKeyboardButton("โฌ ืืืจื โฉ", callback_data=f"buy_category_open:{category_id}:{remover}")
        )

    return keyboard

def get_discount(item_id, category_id, remover, check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("โฌ ะะตัะฝััััั โฉ", callback_data=f"buy_category_open_discout:{category_id}:{remover}"))
    else:
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("โฌ ืืืจื โฉ", callback_data=f"buy_category_open_discout:{category_id}:{remover}"))
    return keyboard

def buy_item(check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("โ", callback_data=f"buy_item_final:yes")).insert(
            InlineKeyboardButton("โ", callback_data=f"buy_item_final:no"))
    else:
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("โ", callback_data=f"buy_item_final:yes")).insert(
            InlineKeyboardButton("โ", callback_data=f"buy_item_final:no"))
    return keyboard
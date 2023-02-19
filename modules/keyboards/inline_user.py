# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton






def select_lang():
    keyboard = InlineKeyboardMarkup(
    ).add(InlineKeyboardButton("🇷🇺 Русский", callback_data="select_lang:ru")
    ).add(InlineKeyboardButton("🇮🇱 עִברִית", callback_data= "select_lang:il"))
    return keyboard
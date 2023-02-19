# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup
from modules.services import db
from modules.utils import main_config

# Кнопки главного меню
def admin__edit_selected(check):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if check == "il":
        keyboard.row("וסף מנהל", "הסר את מנהל המערכת")
        keyboard.row("הצג את רשימת המנהלים", "חזרה לתפריט")
    else:
        keyboard.row("Добавить Администратора", "Удалить Администратора")
        keyboard.row("Посмотреть список Администраторов", "Назад в меню")
    return keyboard

def admin_back(check):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if check == "il":
        keyboard.row("חזור")
    else:
        keyboard.row("Назад")
    return keyboard

def admin__edit_products(check):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if check == "il":
        keyboard.row("📁 צור מוצר ➕", "📁 שנה מוצר 🖍", "📁 מחק את כל המוצרים ❌")
        keyboard.row("🗃 צור קטגוריה ➕", "🗃 שנה קטגוריה 🖍", "🗃 מחק את כל הקטגוריות ❌")
        keyboard.row("⬅ תפריט ראשי")
    else:
        keyboard.row("📁 Создать товар ➕", "📁 Изменить товар 🖍", "📁 Удалить все товары ❌")
        keyboard.row("🗃 Создать категорию ➕", "🗃 Изменить категорию 🖍", "🗃 Удалить все категории ❌")
        keyboard.row("⬅ Главное меню")
    return keyboard



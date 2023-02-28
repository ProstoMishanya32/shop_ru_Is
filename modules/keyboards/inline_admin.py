from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb



def category_edit(category_id, remover, check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("🏷 Изм. название", callback_data=f"category_edit_name:{category_id}:{remover}")
        ).add(
            ikb("⬅ Вернуться ↩", callback_data=f"catategory_edit_swipe:{remover}"),
            ikb("❌ Удалить", callback_data=f"category_edit_delete:{category_id}:{remover}")
 )
    else:
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("🏷 שנה שֵׁם", callback_data=f"category_edit_name:{category_id}:{remover}")
        ).add(
            ikb("⬅ חזרה ↩", callback_data=f"catategory_edit_swipe:{remover}"),
            ikb("❌ מחק", callback_data=f"category_edit_delete:{category_id}:{remover}")
        )
    return keyboard

def category_edit_cancel(category_id, remover, check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ Отменить", callback_data=f"category_edit_open:{category_id}:{remover}"),
        )

    else:
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ בטל", callback_data=f"category_edit_open:{category_id}:{remover}"),
        )
    return keyboard

# Кнопки с удалением категории
def category_edit_delete_selected(category_id, remover, check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ Да, удалить", callback_data=f"category_delete:{category_id}:yes:{remover}"),
            ikb("✅ Нет, отменить", callback_data=f"category_delete:{category_id}:not:{remover}")
        )
    else:
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ כן, מחק", callback_data=f"category_delete:{category_id}:yes:{remover}"),
            ikb("✅ לא, בטל", callback_data=f"category_delete:{category_id}:not:{remover}")
        )
    return keyboard


def category_remove_confirm(check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ Да, удалить все", callback_data="confirm_remove_category:yes"),
            ikb("✅ Нет, отменить", callback_data="confirm_remove_category:not")
        )
    else:
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ כן, מחק הכל", callback_data="confirm_remove_category:yes"),
            ikb("✅ לא, בטל", callback_data="confirm_remove_category:not")
        )
    return keyboard

def item_remove_confirm(check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ Да, удалить все", callback_data="confirm_remove_item:yes"),
            ikb("✅ Нет, отменить", callback_data="confirm_remove_item:not")
        )
    else:
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ כן, מחק הכל", callback_data="confirm_remove_item:yes"),
            ikb("✅ לא, בטל", callback_data="confirm_remove_item:not")
        )
    return keyboard
# Кнопки при открытии позиции для изменения
def item_edit_open(item_id, category_id, remover, check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("🏷 Изменить название", callback_data=f"item_edit_name:{item_id}:{category_id}:{remover}"),
            ikb("💰 Изменить цену", callback_data=f"item_edit_price:{item_id}:{category_id}:{remover}"),
        ).add(
            ikb("📜 Изменить описание", callback_data=f"item_edit_description:{item_id}:{category_id}:{remover}"),
            ikb("📸 Изменить фото", callback_data=f"item_edit_photo:{item_id}:{category_id}:{remover}"),
        ).add(
            ikb("❌ Удалить", callback_data=f"item_edit_delete:{item_id}:{category_id}:{remover}"),
            ikb("⬅ Вернуться ↩", callback_data=f"item_edit_swipe:{item_id}:{remover}"),
        )
    else:
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("🏷 שנה כותרת", callback_data=f"item_edit_name:{item_id}:{category_id}:{remover}"),
            ikb("💰 שנה מחיר", callback_data=f"item_edit_price:{item_id}:{category_id}:{remover}"),
        ).add(
            ikb("📜 ערוך תיאור", callback_data=f"item_edit_description:{item_id}:{category_id}:{remover}"),
            ikb("📸 ערוך תמונה", callback_data=f"item_edit_photo:{item_id}:{category_id}:{remover}"),
        ).add(
            ikb("❌ מחק", callback_data=f"item_edit_delete:{item_id}:{category_id}:{remover}"),
            ikb("⬅ חזרה ↩", callback_data=f"item_edit_swipe:{item_id}:{remover}"),
        )
    return keyboard


def item_edit_delete(item_id, category_id, remover, check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ Да, удалить", callback_data=f"item_delete:yes:{item_id}:{category_id}:{remover}"),
            ikb("✅ Нет, отменить", callback_data=f"item_delete:not:{item_id}:{category_id}:{remover}")
        )
    else:
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ כן, מחק", callback_data=f"item_delete:yes:{item_id}:{category_id}:{remover}"),
            ikb("✅ לא, בטל", callback_data=f"item_delete:not:{item_id}:{category_id}:{remover}")
        )

    return keyboard

# Отмена изменения позиции и возвращение
def item_edit_cancel(position_id, category_id, remover, check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ Отменить", callback_data=f"item_edit_open:{position_id}:{category_id}:{remover}"),
        )
    else:
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ בטל", callback_data=f"item_edit_open:{position_id}:{category_id}:{remover}"),
        )

    return keyboard


def item_edit_clear_all(item_id, category_id, remover, check):
    if check == 'ru':
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ Да, удалить", callback_data=f"item_clear:yes:{item_id}:{category_id}:{remover}"),
            ikb("✅ Нет, отменить", callback_data=f"item_clear:not:{item_id}:{category_id}:{remover}")
        )
    else:
        keyboard = InlineKeyboardMarkup(
        ).add(
            ikb("❌ כן, מחק", callback_data=f"item_clear:yes:{item_id}:{category_id}:{remover}"),
            ikb("✅ לא, בטל", callback_data=f"item_clear:not:{item_id}:{category_id}:{remover}")
        )

    return keyboard


def change_texts(text_category):
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("🇷🇺", callback_data=f"change_text:ru:{text_category}"),
        ikb("🇮🇱", callback_data=f"change_text:il:{text_category}")
    )
    return keyboard


def alerts_confirm():
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("✅", callback_data=f"alerts_confirm:yes"),
        ikb("❌", callback_data=f"alerts_confirm:no")
    )
    return keyboard

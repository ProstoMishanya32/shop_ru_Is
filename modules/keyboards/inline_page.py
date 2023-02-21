import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb
from bot_telegram import dp
from modules.services import db


def category_edit_swipe_(remover, check):
    get_categories = db.get_all_info("category")
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(ikb(get_categories[a]['category_name'],
                             callback_data=f"category_edit_open:{get_categories[a]['category_id']}:{remover}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        if check == 'ru':
            keyboard.add(
                ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"catategory_edit_swipe:{remover + 10}"))
        else:
            keyboard.add(
                ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("נוסף ➡", callback_data=f"catategory_edit_swipe:{remover + 10}"))
    elif remover + 10 >= len(get_categories):
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"catategory_edit_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="...") )
        else:
            keyboard.add(
                ikb("⬅ חזור", callback_data=f"catategory_edit_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="...") )
    else:
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"catategory_edit_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"catategory_edit_swipe:{remover + 10}"), )
        else:
            keyboard.add(
                ikb("⬅ חזור", callback_data=f"catategory_edit_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("נוסף ➡", callback_data=f"catategory_edit_swipe:{remover + 10}"), )
    return keyboard

def items_create_swipe_fp(remover, check):
    get_categories = db.get_all_info("category")
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(ikb(get_categories[a]['category_name'],
                             callback_data=f"item_create_open:{get_categories[a]['category_id']}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        if check == 'ru':
            keyboard.add(
                ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"item_create_swipe:{remover + 10}"),
            )
        else:
            keyboard.add(
                ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("הבא ➡", callback_data=f"item_create_swipe:{remover + 10}"),
            )
    elif remover + 10 >= len(get_categories):
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"item_create_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"item_create_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            )
    else:
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"item_create_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"items_create_swipe:{remover + 10}"),
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"item_create_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("הבא ➡", callback_data=f"item_create_swipe:{remover + 10}"),
            )

    return keyboard


def item_edit_category_swipe_fp(remover, check):
    get_categories = db.get_all_info("category")
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(ikb(get_categories[a]['category_name'],
                             callback_data=f"item_edit_category_open:{get_categories[a]['category_id']}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        if check == 'ru':
            keyboard.add(
                ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"item_edit_category_swipe:{remover + 10}")
            )
        else:
            keyboard.add(
                ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("הבא ➡", callback_data=f"item_edit_category_swipe:{remover + 10}")
            )

    elif remover + 10 >= len(get_categories):
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"item_edit_category_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="...")
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"item_edit_category_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="...")
            )
    else:
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"item_edit_category_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"items_edit_category_swipe:{remover + 10}"),
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"item_edit_category_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("הבא ➡", callback_data=f"items_edit_category_swipe:{remover + 10}"),
            )

    return keyboard



# Стартовые страницы позиций для их изменения
def item_edit_swipe_fp(remover, category_id, check):
    get_items = db.get_all_item(category_id=category_id)
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_items): remover -= 10
    for count, a in enumerate(range(remover, len(get_items))):
        if count < 10:
            keyboard.add(ikb(
                f"{get_items[a]['item_name']} | {get_items[a]['item_price']}₽ ",
                callback_data=f"item_edit_open:{get_items[a]['item_id']}:{category_id}:{remover}"))

    if len(get_items) <= 10:
        pass
    elif len(get_items) > 10 and remover < 10:
        if check == 'ru':
            keyboard.add(
                ikb(f"🔸 1/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"item_edit_swipe:{category_id}:{remover + 10}")
            )
        else:
            keyboard.add(
                ikb(f"🔸 1/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
                ikb("הבא ➡", callback_data=f"item_edit_swipe:{category_id}:{remover + 10}")
            )
    elif remover + 10 >= len(get_items):
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"item_edit_swipe:{category_id}:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_items) / 10)} 🔸", callback_data="...")
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"item_edit_swipe:{category_id}:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_items) / 10)} 🔸", callback_data="...")
            )
    else:
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"item_edit_swipe:{category_id}:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"item_edit_swipe:{category_id}:{remover + 10}"),
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"item_edit_swipe:{category_id}:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
                ikb("הבא ➡", callback_data=f"item_edit_swipe:{category_id}:{remover + 10}"),
            )
    if check == 'ru':
       keyboard.add(ikb("⬅ Вернуться ↩", callback_data="item_edit_category_swipe:0"))
    else:
        keyboard.add(ikb("⬅ חזרה ↩", callback_data="item_edit_category_swipe:0"))

    return keyboard


def item_category_swipe_fp(remover, check):
    get_categories = db.get_all_info('category')
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(ikb(get_categories[a]['category_name'],
                             callback_data=f"buy_category_open:{get_categories[a]['category_id']}:0"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        if check == 'ru':
            keyboard.add(
                ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"buy_category_swipe:{remover + 10}"),
            )
        else:
            keyboard.add(
                ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("הבא ➡", callback_data=f"buy_category_swipe:{remover + 10}"),
            )
    elif remover + 10 >= len(get_categories):
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"buy_category_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"buy_category_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            )
    else:
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"buy_category_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"buy_category_swipe:{remover + 10}"),
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"buy_category_swipe:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("הבא ➡", callback_data=f"buy_category_swipe:{remover + 10}"),
            )
    return keyboard


def item_swipe_fp(remover, category_id, check ):
    get_item = db.get_all_item(category_id=category_id)
    keyboard = InlineKeyboardMarkup()
    if remover >= len(get_item): remover -= 10

    for count, a in enumerate(range(remover, len(get_item))):
        if count < 10:
            keyboard.add(ikb(
                f"{get_item[a]['item_name']} | {get_item[a]['item_price']}₪ ",
                callback_data=f"buy_item_open:{get_item[a]['item_id']}:{category_id}:{remover}"))

    if len(get_item) <= 10:
        pass
    elif len(get_item) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_item) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_item_swipe:{category_id}:{remover + 10}"),
        )
    elif remover + 10 >= len(get_positions):
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"buy_item_swipe:{category_id}:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_item) / 10)} 🔸", callback_data="..."),
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"buy_item_swipe:{category_id}:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_item) / 10)} 🔸", callback_data="..."),
            )
    else:
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"buy_item_swipe:{category_id}:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_item) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"buy_item_swipe:{category_id}:{remover + 10}"),
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"buy_item_swipe:{category_id}:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_item) / 10)} 🔸", callback_data="..."),
                ikb("הבא ➡", callback_data=f"buy_item_swipe:{category_id}:{remover + 10}"),
            )
    if check == 'ru':
        keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_category_swipe:0"))
    else:
        keyboard.add(ikb("⬅ חזרה ↩", callback_data=f"buy_category_swipe:0"))

    return keyboard

def item_category_swipe_fp_discount(remover, check):
    get_categories = db.get_all_info('category')
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(ikb(get_categories[a]['category_name'],
                             callback_data=f"buy_category_open_discout:{get_categories[a]['category_id']}:0"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        if check == 'ru':
            keyboard.add(
                ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"buy_category_swipe_discout:{remover + 10}"),
            )
        else:
            keyboard.add(
                ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("הבא ➡", callback_data=f"buy_category_swipe:{remover + 10}"),
            )
    elif remover + 10 >= len(get_categories):
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"buy_category_swipe_discout:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"buy_category_swipe_discout:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            )
    else:
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"buy_category_swipe_discout:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"buy_category_swipe_discout:{remover + 10}"),
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"buy_category_swipe_discout:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
                ikb("הבא ➡", callback_data=f"buy_category_swipe_discout:{remover + 10}"),
            )
    return keyboard

def item_swipe_fp_discout(remover, category_id, check ):
    get_item = db.get_all_item(category_id=category_id)
    keyboard = InlineKeyboardMarkup()
    if remover >= len(get_item): remover -= 10

    for count, a in enumerate(range(remover, len(get_item))):
        if count < 10:
            keyboard.add(ikb(
                f"{get_item[a]['item_name']} | {get_item[a]['item_price']}₪ ",
                callback_data=f"buy_item_open_discout:{get_item[a]['item_id']}:{category_id}:{remover}"))

    if len(get_item) <= 10:
        pass
    elif len(get_item) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_item) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_item_swipe_discout:{category_id}:{remover + 10}"),
        )
    elif remover + 10 >= len(get_positions):
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"buy_item_swipe_discout:{category_id}:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_item) / 10)} 🔸", callback_data="..."),
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"buy_item_swipe_discout:{category_id}:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_item) / 10)} 🔸", callback_data="..."),
            )
    else:
        if check == 'ru':
            keyboard.add(
                ikb("⬅ Назад", callback_data=f"buy_item_swipe_discout:{category_id}:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_item) / 10)} 🔸", callback_data="..."),
                ikb("Далее ➡", callback_data=f"buy_item_swipe_discout:{category_id}:{remover + 10}"),
            )
        else:
            keyboard.add(
                ikb("⬅ חזרה", callback_data=f"buy_item_swipe_discout:{category_id}:{remover - 10}"),
                ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_item) / 10)} 🔸", callback_data="..."),
                ikb("הבא ➡", callback_data=f"buy_item_swipe_discout:{category_id}:{remover + 10}"),
            )
    if check == 'ru':
        keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_category_swipe_discout:0"))
    else:
        keyboard.add(ikb("⬅ חזרה ↩", callback_data=f"buy_category_swipe_discout:0"))

    return keyboard
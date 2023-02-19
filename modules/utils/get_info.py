from modules.services import db
from modules.utils.const_func import ded

def get_admin_items(items_id, check):
    item = db.get_item(item_id=items_id)
    category = db.get_category(category_id=item['category_id'])

    if check == 'ru':
        text_description = "<code>Отсутствует ❌</code>"
        photo_text = "<code>Отсутствует ❌</code>"
    else:
        text_description = "<code>חסר ❌</code>"
        photo_text = "<code>חסר ❌</code>"
    get_photo = None


    if len(item['item_photo']) >= 5:
        if check == 'ru':
            photo_text = "<code>Присутствует ✅</code>"
        else:
            photo_text = "<code>הווה ✅</code>"
            get_photo = item['item_photo']


    if item['item_description'] != "0":
        text_description = f"\n{item['item_description']}"

    if check == 'ru':
        get_message = ded(f"""
                      <b>📦 Товар: <code>{item['item_name']}</code></b>
                      ➖➖➖➖➖➖➖➖➖➖
                      🗃 Категория: <code>{item['item_name']}</code>
                      💰 Стоимость: <code>{item['item_price']}₽</code>
                      📸 Изображение: {photo_text}
                      📜 Описание: {text_description}""")
    else:
        get_message = ded(f"""
                      <b>📦 פריט: <code>{item['item_name']}</code></b>
                      ➖➖➖➖➖➖➖➖➖➖
                      🗃 קטגוריה: <code>{item['item_name']}</code>
                      💰 מחיר: <code>{item['item_price']}₽</code>
                     📸 תמונה: {photo_text}
       תיאור:               {text_description}""")

    return get_message, get_photo
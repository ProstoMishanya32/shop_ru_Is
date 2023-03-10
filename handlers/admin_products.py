# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageCantBeDeleted, CantParseEntities
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from modules.services import db, json_logic
from bot_telegram import dp
from modules.keyboards import  reply_admin, inline_page, inline_admin, reply_user
from contextlib import suppress
from modules.utils.check_func import CheckAdmin
from handlers import start_user
from modules.utils.const_func import get_unix
from modules.utils.get_info import get_admin_items


@dp.message_handler(CheckAdmin(), text = ['🎁 Управление товарами', '🎁 ניהול מוצר'], state = "*")
async def admin_menu_start(message: Message, state: FSMContext):
    await state.finish()
    check = db.check_user(message.from_user.id)
    if check == 'ru':
        await message.answer("<b>Панель управления товарами</b>", reply_markup=reply_admin.admin__edit_products(check))
    else:
        await message.answer("<b>לוח בקרה של מוצרים</b>", reply_markup=reply_admin.admin__edit_products(check) )

# Создание новой категории
@dp.message_handler(CheckAdmin(), text= ['🗃 Создать категорию ➕', '🗃 צור קטגוריה ➕'], state="*")
async def category_create(message: Message, state: FSMContext):
    await state.finish()
    check = db.check_user(message.from_user.id)
    if check == 'ru':
        await message.answer("<b>Введите название для категории</b>")
    else:
        await message.answer("<b>הזן שם לקטגוריה</b>")
    await state.set_state("category_name")


# Открытие страниц выбора категорий для редактирования
@dp.message_handler(CheckAdmin(), text= ['🗃 Изменить категорию 🖍', '🗃 שנה קטגוריה 🖍'], state="*")
async def category_edit(message: Message, state: FSMContext):
    await state.finish()
    check = db.check_user(message.from_user.id)
    if len(db.get_all_info("category")) >= 1:
        if check == 'ru':
            await message.answer("<b>🗃 Выберите категорию для изменения 🖍</b>", reply_markup= inline_page.category_edit_swipe_(0, check))
        else:
            await message.answer("<b>🗃 בחר קטגוריה לעריכה 🖍</b>",   reply_markup=inline_page.category_edit_swipe_(0, check))
    else:
        if check == 'ru':
            await message.answer("<b>❌ Отсутствуют категории для изменения позиций</b>")
        else:
            await message.answer("<b>❌ אין קטגוריות לשינוי מיקום</b>")


# уточнение удалить все категории
@dp.message_handler(CheckAdmin(), text=['🗃 Удалить все категории ❌', '🗃 מחק את כל הקטגוריות ❌'], state="*")
async def category_remove(message: Message, state: FSMContext):
    await state.finish()
    check = db.check_user(message.from_user.id)
    if check == 'ru':
        await message.answer("<b>Вы действительно хотите удалить все категории? ❌</b>\n"
                             "❗ Так же будут удалены все позиции и товары",  reply_markup=inline_admin.category_remove_confirm(check))
    else:
        await message.answer("<b>האם אתה בטוח שברצונך למחוק את כל הקטגוריות? ❌</b>\n"
                             "❗ כל העמדות והמוצרים יימחקו גם כן",  reply_markup=inline_admin.category_remove_confirm(check))


@dp.message_handler(CheckAdmin(), text=['📁 Создать товар ➕', '📁 צור מוצר ➕'], state="*")
async def item_create(message: Message, state: FSMContext):
    await state.finish()
    check = db.check_user(message.from_user.id)
    if len(db.get_all_info("category")) >= 1:
        if check == 'ru':
            await message.answer("<b>Выберите категорию для товара</b>", reply_markup=inline_page.items_create_swipe_fp(0, check))
        else:
            await message.answer("<b>בחר קטגוריה עבור המוצר</b>", reply_markup=inline_page.items_create_swipe_fp(0, check))
    else:
        if check == 'ru':
            await message.answer("<b>❌ Отсутствуют категории для изменения товара</b>")
        else:
            await message.answer("<b>❌ אין קטגוריות לשינוי המוצר</b>")


# Начальные категории для изменения позиции
@dp.message_handler(CheckAdmin(), text=['📁 Изменить товар 🖍', '📁 שנה מוצר 🖍'], state="*")
async def item_edit(message: Message, state: FSMContext):
    await state.finish()
    check = db.check_user(message.from_user.id)
    if len(db.get_all_info("category")) >= 1:
        if check == 'ru':
            await message.answer("<b>Выберите категорию с нужным товаром 🖍</b>",reply_markup=inline_page.item_edit_category_swipe_fp(0, check))
        else:
            await message.answer("<b>Выберите категорию с нужным товаром 🖍</b>",reply_markup=inline_page.item_edit_category_swipe_fp(0, check))
    else:
        if check == 'ru':
            await message.answer("<b>❌ Отсутствуют категории для изменения товара</b>")
        else:
            await message.answer("<b>❌ אין קטגוריות לשינוי המוצר</b>")



@dp.message_handler(CheckAdmin(), text= ['📁 Удалить все товары ❌', '📁 מחק את כל המוצרים ❌'], state="*")
async def item_remove(message: Message, state: FSMContext):
    await state.finish()
    check = db.check_user(message.from_user.id)
    if check == 'ru':
        await message.answer("<b>Вы действительно хотите удалить все товары? ❌</b>\n", reply_markup=inline_admin.item_remove_confirm(check))
    else:
        await message.answer("<b>האם אתה בטוח שברצונך למחוק את כל המוצרים? ❌</b>\n", reply_markup=inline_admin.item_remove_confirm(check))

@dp.message_handler(CheckAdmin(), text= ['⬅ Главное меню', '⬅ תפריט ראשי'], state="*")
async def exit_menu(message: Message, state: FSMContext):
    await state.finish()
    check = db.check_user(message.from_user.id)
    if check == 'ru':
        await message.answer("<b>➖➖➖Добро пожаловать в меню 🏠➖➖➖</b>\n\n"
                             "🔶 Если не появились вспомогательные кнопки\n"
                             "▶️ Введите /start", reply_markup=reply_user.menu((message.from_user.id)))
    else:
        await message.answer("<b>➖➖➖ברוכים הבאים לתפריט 🏠➖➖➖</b>\n\n"
                             "🔶 אם לחצני עזר לא מופיעים\n"
                             "▶️ הקלד / התחל", reply_markup=reply_user.menu((message.from_user.id)))


####################################
#Создание категории
@dp.message_handler(CheckAdmin(), state="category_name")
async def category_create_name(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    if len(message.text) <= 50:
        category_id = get_unix()
        db.add_category(category_id, message.text)
        await state.finish()

        try:
            items = len(db.get_item(category_id=category_id))
        except TypeError:
            items = 0
        category = db.get_category(category_id=category_id)

        if check == 'ru':
            await message.answer("➖➖➖➖<b>Категория создана!</b>➖➖➖➖\n"
                                f"<b>🗃 Категория: <code>{category['category_name']}</code></b>\n"
                                 "➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                 f"📦 Кол-во товаров: <code>{items}шт</code>",  reply_markup=inline_admin.category_edit(category_id, 0, check))
        else:
            await message.answer("➖➖➖➖<b>הקטגוריה נוצרה!</b>➖➖➖➖"
                                 f"<b>🗃 קטגוריה: <code>{category['category_name']}</code></b>\n"
                                 "➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                 f"📦 Кол-во товаров: <code>{items}шт</code>",  reply_markup=inline_admin.category_edit(category_id, 0, check))  # КНОПКА, приделать
    else:
        if check == 'ru':
            await message.answer("<b>❌ Название не может превышать 50 символов.</b>\n"
                                 "🗃 Введите название для категории 🏷")
        else:
            await message.answer("<b>❌ הכותרת לא יכולה לעלות על 50 תווים.</b>\n"
                                 "🗃 הזינו שם לקטגוריה 🏷")



# Страница выбора категорий для редактирования
@dp.callback_query_handler(CheckAdmin(), text_startswith="catategory_edit_swipe:", state="*")
async def product_category_edit_swipe(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    check = db.check_user(call.from_user.id)
    if check == 'ru':
        await call.message.edit_text("<b>Выберите категорию для изменения</b>",reply_markup=inline_page.category_edit_swipe_(remover, check))
    else:
        await call.message.edit_text("<b>בחר קטגוריה לעריכה</b>",
                                     reply_markup=inline_page.category_edit_swipe_(remover, check))


@dp.callback_query_handler(CheckAdmin(), text_startswith="category_edit_open:", state="*")
async def product_category_edit_open(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    await state.finish()
    check = db.check_user(call.from_user.id)
    try:
        items = len(db.get_item(category_id=category_id))
    except TypeError:
        items = 0
    category = db.get_category(category_id=category_id)

    if check == 'ru':
        await call.message.edit_text(f"<b>🗃 Категория: <code>{category['category_name']}</code></b>\n"
                                     "➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                     f"📦 Кол-во товаров: <code>{items}шт</code>",
                                     reply_markup=inline_admin.category_edit(category_id, remover, check))
    else:
        await call.message.answer("➖➖➖➖<b>הקטגוריה נוצרה!</b>➖➖➖➖"
                             f"<b>🗃 קטגוריה: <code>{category['category_name']}</code></b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             f"📦 Кол-во товаров: <code>{items}шт</code>",
                             reply_markup=inline_admin.category_edit(category_id, 0, check))

###########################################
#Редактирование категории #################
@dp.callback_query_handler(CheckAdmin(), text_startswith="category_edit_name:", state="*")
async def сategory_edit_name(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    check = db.check_user(call.from_user.id)
    await state.update_data(cache_category_id=category_id)
    await state.update_data(cache_category_remover=remover)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    await state.set_state("change_category_name")
    if check == 'ru':
        await call.message.answer("<b>🗃 Введите новое название для категории 🏷</b>", reply_markup=inline_admin.category_edit_cancel(category_id, remover, check))
    else:
        await call.message.answer("<b>🗃 הזן שם חדש לקטגוריה 🏷</b>", reply_markup=inline_admin.category_edit_cancel(category_id, remover, check))

@dp.message_handler(CheckAdmin(), state="change_category_name")
async def category_edit_name_get(message: Message, state: FSMContext):
    category_id = (await state.get_data())['cache_category_id']
    remover = (await state.get_data())['cache_category_remover']
    check = db.check_user(message.from_user.id)
    if len(message.text) <= 50:
        await state.finish()

        db.update_category(category_id, category_name= message.text)
        try:
            items = len(db.get_item(category_id=category_id))
        except TypeError:
            items = 0
        category = db.get_category(category_id=category_id)

        if check == 'ru':
            await message.answer(f"<b>🗃 Категория: <code>{category['category_name']}</code></b>\n"
                                 "➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                 f"📦 Кол-во товаров: <code>{items}шт</code>",  reply_markup=inline_admin.category_edit(category_id, remover, check))
        else:
            await message.answer(f"<b>🗃 קטגוריה: <code>{category['category_name']}</code></b>\n"
                                 "➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                 f"📦 מספר פריטים: <code>{items}pcs</code>",  reply_markup=inline_admin.category_edit(category_id, remover, check))
    else:
        if check == 'ru':
            await message.answer("<b>❌ Название не может превышать 50 символов.</b>\n"
                                 "🗃 Введите новое название для категории 🏷",
                                 reply_markup=inline_admin.category_edit_cancel(category_id, remover, check))
        else:
            await message.answer("<b>❌ הכותרת לא יכולה לעלות על 50 תווים.</b>\n"
                                 "🗃 הזינו שם חדש לקטגוריה 🏷",
                                 reply_markup=inline_admin.category_edit_cancel(category_id, remover, check))

@dp.callback_query_handler(CheckAdmin(), text_startswith="category_edit_delete:", state="*")
async def category_edit_delete(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    check = db.check_user(call.from_user.id)
    if check == 'ru':
        await call.message.edit_text("<b>❗ Вы действительно хотите удалить категорию и все её данные?</b>", reply_markup=inline_admin.category_edit_delete_selected(category_id, remover, check))
    else:
        await call.message.edit_text("<b>❗ האם אתה בטוח שברצונך למחוק את הקטגוריה ואת כל הנתונים שלה?</b>",reply_markup=inline_admin.category_edit_delete_selected(category_id, remover, check))

# Выбор удаление или нет
@dp.callback_query_handler(CheckAdmin(), text_startswith="category_delete:", state="*")
async def product_category_edit_delete_confirm(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    selected = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])
    check = db.check_user(call.from_user.id)

    if selected == "yes":
        db.delete_category(category_id=category_id)
        db.delete_items(category_id=category_id)

        if check == 'ru':
            await call.answer("🗃 Категория и все её данные были успешно удалены ✅")
        else:
            await call.answer("🗃 הקטגוריה וכל הנתונים שלה נמחקו בהצלחה ✅")
        if len(db.get_all_info("category")) >= 1:
            if check == 'ru':
                await call.message.edit_text("<b>🗃 Выберите категорию для изменения 🖍</b>", reply_markup=inline_page.category_edit_swipe_(remover, check))
            else:
                await call.message.edit_text("<b>🗃 בחר קטגוריה לעריכה 🖍</b>", reply_markup=inline_page.category_edit_swipe_(remover, check))
        else:
            with suppress(MessageCantBeDeleted):
                await call.message.delete()

    else:
        try:
            items = len(db.get_item(category_id=category_id))
        except TypeError:
            items = 0
        category = db.get_category(category_id=category_id)

        if check == 'ru':
            await message.answer(f"<b>🗃 Категория: <code>{category['category_name']}</code></b>\n"
                                 "➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                 f"📦 Кол-во товаров: <code>{items}шт</code>",  reply_markup=inline_admin.category_edit(category_id, remover, check))
        else:
            await message.answer(f"<b>🗃 קטגוריה: <code>{category['category_name']}</code></b>\n"
                                 "➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                 f"📦 מספר פריטים: <code>{items}pcs</code>",  reply_markup=inline_admin.category_edit(category_id, remover, check))

@dp.callback_query_handler(CheckAdmin(), text_startswith="confirm_remove_category:", state="*")
async def category_remove_confirm(call: CallbackQuery, state: FSMContext):
    selected = call.data.split(":")[1]
    check = db.check_user(call.from_user.id)
    if selected == "yes":
        try:
            items = len(db.get_all_info("items"))
            category = len(db.get_all_info("category"))

        except TypeError:
            items = 0
            category = 0

        db.clear_all_category()
        db.clear_add_items()

        if check == 'ru':
            await call.message.edit_text(f"<b>🗃 Вы удалили все категории<code>({category}шт)</code>, товары<code>({items}шт)</code> ☑</b>")
        else:
            await call.message.edit_text(f"<b>🗃 מחקת את כל הקטגוריות<code>({category}pcs)</code>, מוצרים<code>({items}pcs)</code> ☑</b>")
    else:
        if check == 'ru':
            await call.message.edit_text("<b>🗃 Вы отменили удаление всех категорий ✅</b>")
        else:
            await call.message.edit_text("<b>🗃 ביטלת את המחיקה של כל הקטגוריות ✅</b>")

#ДОБАВЛЕНИЕ ПОЗИЦИЙ
@dp.callback_query_handler(CheckAdmin(), text_startswith="item_create_swipe:", state="*")
async def items_create_swipe(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    check = db.check_user(call.from_user.id)
    if check == 'ru':
        await call.message.edit_text("<b>📦 Выберите категорию для товара ➕</b>", reply_markup=inline_page.items_create_swipe_fp(remover, check))
    else:
        await call.message.edit_text("<b>📦 Выберите категорию для товара ➕</b>", reply_markup=inline_page.items_create_swipe_fp(remover, check))

# Выбор категории для создания позиции
@dp.callback_query_handler(CheckAdmin(), text_startswith="item_create_open:", state="*")
async def items_create_select_category(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    check = db.check_user(call.from_user.id)
    await state.update_data(cache_change_category_id=category_id)

    await state.set_state("items_name")
    if check == 'ru':
        await call.message.edit_text("<b>📦 Введите название для товара 🏷</b>")
    else:
        await call.message.edit_text("<b>📦 הזן שם למוצר 🏷</b>")

# Принятие имени для создания позиции
@dp.message_handler(CheckAdmin(), state="items_name")
async def items_create_name(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    if len(message.text) <= 50:
        await state.update_data(items_name=message.text)
        await state.set_state("position_price")
        if check == 'ru':
            await message.answer("<b>📦 Введите цену для товара 💰</b>")
        else:
            await message.answer("<b>📦 הזן מחיר לפריט 💰</b>")
    else:
        if check == 'ru':
            await message.answer("<b>❌ Название не может превышать 50 символов.</b>\n"
                                 "📦 Введите название для товара 🏷")
        else:
            await message.answer("<b>❌ הכותרת לא יכולה לעלות על 50 תווים.</b>\n"
                                 "📦 הזינו שם למוצר 🏷")

# Принятие цены позиции для её создания
@dp.message_handler(CheckAdmin(), state="position_price")
async def items_create_price(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    if message.text.isdigit():
        if 0 <= int(message.text) <= 10000000:
            await state.update_data(items_price=message.text)

            await state.set_state("items_description")
            if check == 'ru':
                await message.answer("<b>📦 Введите описание для товара 📜</b>\n"
                                     "❕ Вы можете использовать HTML разметку\n"
                                     "❕ Отправьте <code>0</code> чтобы пропустить.")
            else:
                await message.answer("<b>📦 הזן תיאור עבור הפריט 📜</b>\n"
                                     "❕ אתה יכול להשתמש בסימון HTML\n"
                                     "❕ שלח את <code>0</code> כדי לדלג.")
        else:
            if check == 'ru':
                await message.answer("<b>❌ Цена не может быть меньше 0₽ или больше 10 000 000₽.</b>\n"
                                     "📦 Введите цену для товара 💰")
            else:
                await message.answer("<b>❌ המחיר לא יכול להיות פחות מ-0₽ או יותר מ-10,000,000₽.</b>\n"
                                     "📦 הכניסו מחיר למוצר 💰")
    else:
        if check == 'ru':
            await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                                 "📦 Введите цену для товара 💰")
        else:
            await message.answer("<b>❌ הנתונים הוזנו בצורה שגויה.</b>\n"
                                 "📦 הכניסו מחיר למוצר 💰")


# Принятие описания позиции для её создания
@dp.message_handler(CheckAdmin(), state="items_description")
async def items_create_description(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    try:
        if len(message.text) <= 600:
            if message.text != "0":
                cache_msg = await message.answer(message.text)
                await cache_msg.delete()

            await state.update_data(items_description=message.text)

            await state.set_state("items_photo")
            if check == 'ru':
                await message.answer("<b>📦 Отправьте изображение для товара 📸</b>\n"
                                    "❕ Отправьте <code>0</code> чтобы пропустить.")
            else:
                await message.answer("<b>📦 שלח תמונת מוצר 📸</b>\n"
                                    "❕ שלח את <code>0</code> כדי לדלג.")
        else:
            if check == 'ru':
                await message.answer("<b>❌ Описание не может превышать 600 символов.</b>\n"
                                     "📦 Введите новое описание для товара 📜\n"
                                     "❕ Вы можете использовать HTML разметку\n"
                                     "❕ Отправьте <code>0</code> чтобы пропустить.")
            else:
                await message.answer("<b>❌ התיאור אינו יכול לעלות על 600 תווים.</b>\n"
                                     "📦 הזינו תיאור חדש למוצר 📜\n"
                                     "❕ אתה יכול להשתמש בסימון HTML\n"
                                     "❕ שלח את <code>0</code> כדי לדלג.")
    except CantParseEntities:
        if check == 'ru':
            await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                                 "📦 Введите описание для товара 📜\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.")
        else:
            await message.answer("<b>❌ שגיאת תחביר HTML.</b>\n"
                                 "📦 הזן תיאור לפריט 📜\n"
                                 "❕ אתה יכול להשתמש בסימון HTML\n"
                                 "❕ שלח את <code>0</code> כדי לדלג.")


@dp.message_handler(CheckAdmin(), content_types="photo", state="items_photo")
@dp.message_handler(CheckAdmin(), text="0", state="items_photo")
async def items_create_photo(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    async with state.proxy() as data:
        items_name = data['items_name']
        items_price = data['items_price']
        category_id = data['cache_change_category_id']
        items_description = data['items_description']
    await state.finish()

    items_photo = ""

    if "text" not in message:
        items_photo = message.photo[-1].file_id

    item_id = db.add_items(items_name, items_price, items_description, items_photo, category_id)
    get_message, get_photo = get_admin_items(item_id, check)

    if get_photo is not None:
        await message.answer_photo(get_photo, get_message, reply_markup=inline_admin.item_edit_open(item_id, category_id, 0, check))
    else:
        await message.answer(get_message, reply_markup=inline_admin.item_edit_open(item_id, category_id, 0, check))

#ИЗМЕНЕНИЕ ТОВАРА

# Выбор категории с нужным товаром
@dp.callback_query_handler(CheckAdmin(), text_startswith="item_edit_category_open:", state="*")
async def item_edit_category_open(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    check = db.check_user(call.from_user.id)
    get_category = db.get_category(category_id=category_id)
    get_items = db.get_item(category_id=category_id)

    if len(get_items) >= 1:
        if check == 'ru':
            await call.message.edit_text("<b>📦 Выберите нужный вам товар 🖍</b>",
                                         reply_markup=inline_page.item_edit_swipe_fp(0, category_id, check))
        else:
            await call.message.edit_text("<b>📦 בחר את המוצר שאתה צריך 🖍</b>",
                                         reply_markup=inline_page.item_edit_swipe_fp(0, category_id, check))
    else:
        if check == 'ru':
            await call.answer(f"📦 Товаров в категории {get_category['category_name']} нет")
        else:
            await call.answer(f"📦 אין מוצרים בקטגוריה {get_category['category_name']}")


# Перемещение по страницам категорий для редактирования позиции
@dp.callback_query_handler(CheckAdmin(), text_startswith="item_edit_category_swipe:", state="*")
async def item_edit_category_swipe(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    check = db.check_user(call.from_user.id)

    if check == 'ru':
        await call.message.edit_text("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                                     reply_markup=inline_page.item_edit_category_swipe_fp(remover, check))
    else:
        await call.message.edit_text("<b>📁 בחר את הקטגוריה עם המיקום הרצוי 🖍</b>",
                                     reply_markup=inline_page.item_edit_category_swipe_fp(remover, check))



@dp.callback_query_handler(CheckAdmin(), text_startswith="item_edit_open:", state="*")
async def product_position_edit_open(call: CallbackQuery, state: FSMContext):
    item_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])
    check = db.check_user(call.from_user.id)

    get_message, get_photo = get_admin_items(item_id, check)
    await state.finish()

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    if get_photo is not None:
        await call.message.answer_photo(get_photo, get_message,  reply_markup=inline_admin.item_edit_open(item_id, category_id, remover, check))
    else:
        await call.message.answer(get_message,  reply_markup=inline_admin.item_edit_open(item_id, category_id, remover, check))

@dp.callback_query_handler(CheckAdmin(), text_startswith="item_edit_swipe:", state="*")
async def item_edit_swipe(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    check = db.check_user(call.from_user.id)
    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    if check == 'ru':
        await call.message.answer("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                                     reply_markup=inline_page.item_edit_category_swipe_fp(remover, check))
    else:
        await call.message.answer("<b>📁 בחר את הקטגוריה עם המיקום הרצוי 🖍</b>",
                                     reply_markup=inline_page.item_edit_category_swipe_fp(remover, check))


# Изменение имени позиции
@dp.callback_query_handler(CheckAdmin(), text_startswith="item_edit_name:", state="*")
async def item_edit_name(call: CallbackQuery, state: FSMContext):
    item_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])
    check = db.check_user(call.from_user.id)
    await state.update_data(cache_item_id=item_id)
    await state.update_data(cache_category_id=category_id)
    await state.update_data(cache_item_remover=remover)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    await state.set_state("change_item_name")
    if check == 'ru':
        await call.message.answer("<b>📦 Введите новое название для позиции 🏷</b>", reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))
    else:
        await call.message.answer("<b>📦 הזן שם חדש לתפקיד 🏷</b>", reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))

#Окончательное смена имени
@dp.message_handler(CheckAdmin(), state="change_item_name")
async def item_edit_name_get(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    async with state.proxy() as data:
        item_id = data['cache_item_id']
        category_id = data['cache_category_id']
        remover = data['cache_item_remover']

    if len(message.text) <= 50:
        await state.finish()

        db.update_items(item_id, item_name= message.text)
        get_message, get_photo = get_admin_items(item_id, check)

        if get_photo is not None:
            await message.answer_photo(get_photo, get_message,  reply_markup=inline_admin.item_edit_open(item_id, category_id, remover, check))
        else:
            await message.answer(get_message, reply_markup=inline_admin.item_edit_open(item_id, category_id, remover, check))
    else:
        if check == 'ru':
            await message.answer("<b>❌ Название не может превышать 50 символов.</b>\n"
                                 "📦 Введите новое название для товара 🏷",
                                 reply_markup=inline_admin.item_edit_cancel(position_id, category_id, remover, check))
        else:
            await message.answer("<b>❌ הכותרת לא יכולה לעלות על 50 תווים.</b>\n"
                                 "📦 הזינו שם מוצר חדש 🏷",
                                 reply_markup=inline_admin.item_edit_cancel(position_id, category_id, remover, check))


# Изменение цены товара
@dp.callback_query_handler(CheckAdmin(), text_startswith="item_edit_price:", state="*")
async def item_edit_price(call: CallbackQuery, state: FSMContext):
    item_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])
    check = db.check_user(call.from_user.id)

    await state.update_data(cache_item_id=item_id)
    await state.update_data(cache_category_id=category_id)
    await state.update_data(cache_item_remover=remover)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    await state.set_state("change_item_price")

    if check == 'ru':
        await call.message.answer("<b>📦 Введите новую цену для товара 💰</b>",reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))
    else:
        await call.message.answer("<b>📦 הזן מחיר חדש לפריט 💰</b>",reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))

# Принятие цены позиции для её изменения
@dp.message_handler(CheckAdmin(), state="change_item_price")
async def item_edit_price_get(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    async with state.proxy() as data:
        item_id = data['cache_item_id']
        category_id = data['cache_category_id']
        remover = data['cache_item_remover']

    if message.text.isdigit():
        if 0 <= int(message.text) <= 10000000:
            await state.finish()

            db.update_items(item_id, item_price=message.text)
            get_message, get_photo = get_admin_items(item_id, check)

            if get_photo is not None:
                await message.answer_photo(get_photo, get_message, reply_markup=inline_admin.item_edit_open(item_id, category_id, remover, check))
            else:
                await message.answer(get_message,  reply_markup=inline_admin.item_edit_open(item_id, category_id, remover, check))
        else:
            if check == 'ru':
                await message.answer("<b>❌ Цена не может быть меньше 0₽ или больше 10 000 000₽.</b>\n"
                                     "📦 Введите цену для товара 💰",
                                     reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))
            else:
                await message.answer("<b>❌ המחיר לא יכול להיות פחות מ-0₽ או יותר מ-10,000,000₽.</b>\n"
                                     "📦 הכניסו מחיר למוצר 💰",
                                     reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))
    else:
        if check == 'ru':
            await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                                 "📦 Введите цену для товара 💰",
                                 reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))
        else:
            await message.answer("<b>❌ הנתונים הוזנו בצורה שגויה.</b>\n"
                                 "📦 הכניסו מחיר למוצר 💰",
                                 reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))

@dp.callback_query_handler(CheckAdmin(), text_startswith="item_edit_description:", state="*")
async def item_edit_description(call: CallbackQuery, state: FSMContext):
    item_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])
    check = db.check_user(call.from_user.id)
    await state.update_data(cache_item_id=item_id)
    await state.update_data(cache_category_id=category_id)
    await state.update_data(cache_item_remover=remover)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()


    await state.set_state("change_item_description")
    if check == 'ru':
        await call.message.answer("<b>📦 Введите новое описание для товара 📜</b>\n"
                                  "❕ Вы можете использовать HTML разметку\n"
                                  "❕ Отправьте <code>0</code> чтобы пропустить.",
                                  reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))
    else:
        await call.message.answer("<b>📦 הזן תיאור חדש עבור הפריט 📜</b>\n"
                                  "❕ אתה יכול להשתמש בסימון HTML\n"
                                  "❕ שלח את <code>0</code> כדי לדלג.",
                                  reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))

# Окончательное изменение описания товара
@dp.message_handler(CheckAdmin(), state="change_item_description")
async def item_edit_description_get(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    async with state.proxy() as data:
        category_id = data['cache_category_id']
        item_id = data['cache_item_id']
        remover = data['cache_item_remover']

    try:
        if len(message.text) <= 600:
            await state.finish()

            if message.text != "0":
                cache_msg = await message.answer(message.text)
                await cache_msg.delete()

            db.update_items(item_id, item_description=message.text)
            get_message, get_photo = get_admin_items(item_id, check)

            if get_photo is not None:
                await message.answer_photo(get_photo, get_message, reply_markup=inline_admin.item_edit_open(item_id, category_id, remover, check))
            else:
                await message.answer(get_message, reply_markup=inline_admin.item_edit_open(item_id, category_id, remover, check))
        else:
            if check == 'ru':
                await message.answer("<b>❌ Описание не может превышать 600 символов.</b>\n"
                                     "📦 Введите новое описание для товара 📜\n"
                                     "❕ Вы можете использовать HTML разметку\n"
                                     "❕ Отправьте <code>0</code> чтобы пропустить.",
                                     reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))
            else:
                await message.answer("<b>❌ התיאור אינו יכול לעלות על 600 תווים.</b>\n"
                                     "📦 הזינו תיאור חדש למוצר 📜\n"
                                     "❕ אתה יכול להשתמש בסימון HTML\n"
                                     "❕ שלח את <code>0</code> כדי לדלג.",
                                     reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))

    except CantParseEntities:
        if check == 'ru':
            await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                                 "📦 Введите новое описание для товара 📜\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.",
                                 reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))
        else:
            await message.answer("<b>❌ שגיאת תחביר HTML.</b>\n"
                                 "📦 הזינו תיאור חדש למוצר 📜\n"
                                 "❕ אתה יכול להשתמש בסימון HTML\n"
                                 "❕ שלח את <code>0</code> כדי לדלג.",
                                 reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))


@dp.callback_query_handler(CheckAdmin(), text_startswith="item_edit_photo:", state="*")
async def item_edit_photo(call: CallbackQuery, state: FSMContext):
    check = db.check_user(call.from_user.id)
    item_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.update_data(cache_item_id=item_id)
    await state.update_data(cache_category_id=category_id)
    await state.update_data(cache_item_remover=remover)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    await state.set_state("change_item_photo")
    if check == 'ru':
        await call.message.answer("<b>📦 Отправьте новое изображение для товара 📸</b>\n"
                                  "❕ Отправьте <code>0</code> чтобы пропустить.",
                                  reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))
    else:
        await call.message.answer("<b>📦 שלח תמונת מוצר חדשה 📸</b>\n"
                                  "❕ שלח את <code>0</code> כדי לדלג.",
                                  reply_markup=inline_admin.item_edit_cancel(item_id, category_id, remover, check))

@dp.message_handler(CheckAdmin(), content_types="photo", state="change_item_photo")
@dp.message_handler(CheckAdmin(), text="0", state="change_item_photo")
async def item_edit_photo_get(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    async with state.proxy() as data:
        item_id = data['cache_item_id']
        category_id = data['cache_category_id']
        remover = data['cache_item_remover']
    await state.finish()

    if "text" in message:
        item_photo = ""
    else:
        item_photo = message.photo[-1].file_id

    db.update_items(item_id, item_photo=item_photo)
    get_message, get_photo = get_admin_items(item_id, check)

    if get_photo is not None:
        await message.answer_photo(get_photo, get_message, reply_markup=inline_admin.item_edit_open(item_id, category_id, remover, check))
    else:
        await message.answer(get_message, reply_markup=inline_admin.item_edit_open(item_id, category_id, remover, check))




@dp.callback_query_handler(CheckAdmin(), text_startswith="item_edit_delete:", state="*")
async def item_edit_delete(call: CallbackQuery, state: FSMContext):
    item_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])
    check = db.check_user(call.from_user.id)
    with suppress(MessageCantBeDeleted):
        await call.message.delete()
    if check == 'ru':
        await call.message.answer("<b>📦 Вы действительно хотите удалить товар? ❌</b>",
                                  reply_markup=inline_admin.item_edit_delete(item_id, category_id, remover, check))
    else:
        await call.message.answer("<b>📦 האם אתה בטוח שברצונך למחוק את המוצר? ❌</b>",
                                  reply_markup=inline_admin.item_edit_delete(item_id, category_id, remover, check))

@dp.callback_query_handler(CheckAdmin(), text_startswith="item_delete:", state="*")
async def item_edit_delete_confirm(call: CallbackQuery, state: FSMContext):
    selected = call.data.split(":")[1]
    item_id = call.data.split(":")[2]
    category_id = call.data.split(":")[3]
    check = db.check_user(call.from_user.id)
    remover = int(call.data.split(":")[4])

    if selected == "yes":
        db.delete_items(item_id=item_id)
        if check == 'ru':
            await call.answer("📦 Вы успешно удалили товар✅")
        else:
            await call.answer("📦 מחקת בהצלחה את הפריט✅")

        if len(db.get_item(category_id=category_id)) >= 1:
            if check == 'ru':
                await call.message.edit_text("<b>📦 Выберите нужный вам товар 🖍</b>",reply_markup=inline_page.item_edit_category_swipe_fp(remover, category_id))
            else:
                await call.message.edit_text("<b>📦 בחר את המוצר שאתה צריך 🖍</b>",  reply_markup=inline_page.item_edit_category_swipe_fp(remover, category_id))
        else:
            with suppress(MessageCantBeDeleted):
                await call.message.delete()
    else:
        get_message, get_photo = get_admin_items(item_id, check)

        with suppress(MessageCantBeDeleted):
            await call.message.delete()

        if get_photo is not None:
            await call.message.answer_photo(get_photo, get_message,
                                            reply_markup=inline_admin.item_edit_open(item_id, category_id, remover, check))
        else:
            await call.message.answer(get_message, reply_markup=inline_admin.item_edit_open(item_id, category_id, remover, check))


@dp.callback_query_handler(CheckAdmin(), text_startswith="confirm_remove_item:", state="*")
async def item_remove_confirm(call: CallbackQuery, state: FSMContext):
    selected = call.data.split(":")[1]
    check = db.check_user(call.from_user.id)
    if selected == "yes":
        try:
            items = len(db.get_all_info("items"))

        except TypeError:
            items = 0
            category = 0

        db.clear_add_items()

        if check == 'ru':
            await call.message.edit_text(f"<b>📦 Вы удалили все товары<code>({items}шт)</code> ☑</b>")
        else:
            await call.message.edit_text(f"<b>📦 מחקת את כל הפריטים<code>({items}pcs)</code> ☑</b>")
    else:
        if check == 'ru':
            await call.message.edit_text("<b>📦 Вы отменили удаление всех товаров ✅</b>")
        else:
            await call.message.edit_text("<b>📦 Вы отменили удаление всех товаров ✅</b>")

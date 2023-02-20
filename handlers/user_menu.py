# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageCantBeDeleted
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from modules.services import db
from bot_telegram import dp
from modules.keyboards import inline_user, reply_user, inline_page
from contextlib import suppress
from modules.utils.const_func import ded

@dp.message_handler(text = ['🇮🇱 Сменить язык 🇷🇺', '🇮🇱 שנה שפה 🇷🇺', '/changelang'], state = "*")
async def change_select(message: Message, state: FSMContext):
    await message.answer("<b>Выберите язык 🇷🇺\n"
                         "➖➖➖➖➖➖\n"
                         " 🇮🇱 בחר שפה </b>", reply_markup=inline_user.select_lang())


#ПОКУПКА ТОВАРА
@dp.message_handler(text = ['🎁 Каталог', '🎁 קטלוג'], state="*")
async def user_shop(message: Message, state: FSMContext):
    await state.finish()
    check = db.check_user(message.from_user.id)

    if len(db.get_all_info('category')) >= 1:
        if check == 'ru':
            await message.answer("<b>🎁 Выберите категорию товара:</b>",  reply_markup=inline_page.item_category_swipe_fp(0, check))
        else:
            await message.answer("<b>🎁 בחר קטגוריית מוצרים:</b>",  reply_markup=inline_page.item_category_swipe_fp(0, check))
    else:
        if check == 'ru':
            await message.answer("<b>🎁 Увы, товары в данное время отсутствуют.</b>")
        else:
            await message.answer("<b>🎁 אבוי, כרגע אין מוצרים.</b>")



@dp.callback_query_handler(text_startswith="buy_category_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    check = db.check_user(call.from_user.id)
    if check == 'ru':
        await call.message.edit_text("<b>🎁 Выберите категорию товара:</b>", reply_markup=inline_page.item_category_swipe_fp(remover, check))
    else:
        await call.message.edit_text("<b>🎁 בחר קטגוריית מוצרים:</b>", reply_markup=inline_page.item_category_swipe_fp(remover, check))


# Открытие категории для покупки
@dp.callback_query_handler(text_startswith="buy_category_open:", state="*")
async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    check = db.check_user(call.from_user.id)

    get_category = db.get_category(category_id=category_id)
    get_item = db.get_item(category_id=category_id)

    if len(get_item) >= 1:
        with suppress(MessageCantBeDeleted):
            await call.message.delete()
        if check == 'ru':
            await call.message.answer(f"<b>🎁 Текущая категория: <code>{get_category['category_name']}</code></b>", reply_markup=inline_page.item_swipe_fp(remover, category_id, check))
        else:
            await call.message.answer(f"<b>🎁 קטגוריה נוכחית: <code>{get_category['category_name']}</code></b>", reply_markup=inline_page.item_swipe_fp(remover, category_id, check))
    else:
        if remover == "0":
            if check == 'ru':
                await call.message.edit_text("<b>🎁 Увы, товары в данное время отсутствуют.</b>")
                await call.answer("❗ Товары были изменены или удалены")
            else:
                await call.message.edit_text("<b>🎁 אבוי, כרגע אין מוצרים.</b>")
                await call.answer("❗ Товары были изменены или удалены")
        else:
            if check == 'ru':
                await call.answer(f"❕ Товары в категории {get_category['category_name']} отсутствуют")
            else:
                await call.answer(f"❕ אין מוצרים בקטגוריה {get_category['category_name']}")

@dp.callback_query_handler(text_startswith="buy_item_open:", state="*")
async def user_purchase_position_open(call: CallbackQuery, state: FSMContext):
    item_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    check = db.check_user(call.from_user.id)
    get_item = db.get_item(item_id=item_id)
    get_category = db.get_category(category_id=category_id)

    if get_item['item_description'] == "0":
        text_description = ""
    else:
        if check == 'ru':
            text_description = f"\n📜 Описание:\n{get_item['item_description']}"
        else:
            text_description = f"\n📜 Описание:\n{get_item['item_description']}"

    if check == 'ru':
        send_msg = ded(f"""
                   <b>🎁 Покупка товара:</b>
                   ➖➖➖➖➖➖➖➖➖➖
                   🏷 Название: <code>{get_item['item_name']}</code>
                   🗃 Категория: <code>{get_category['category_name']}</code>
                   💰 Стоимость: <code>{get_item['item_price']}₪</code>
                   {text_description}
                   """)
    else:
        send_msg = (
                    f"<b>🎁 רכישת מוצר:</b>\n"
                    f"➖➖➖➖➖➖➖➖➖➖\n"
                    f"🏷 שם: <code>{get_item['item_name']}</code>\n"
                    f"🗃 קטגוריה: <code> {get_category['category_name']}</code>\n"
                    f"💰 עלות: <code>{get_item['item_price']}₪</code>\n"
                    f"{text_description}"
                   )

    if len(get_item['item_photo']) >= 5:
        with suppress(MessageCantBeDeleted):
            await call.message.delete()
        await call.message.answer_photo(get_item['item_photo'],send_msg, reply_markup=inline_user.item_open(item_id, category_id, remover, check))
    else:
        await call.message.edit_text(send_msg, reply_markup=inline_user.item_open(item_id, category_id, remover, check))


@dp.callback_query_handler(text_startswith="buy_item_swipe:", state="*")
async def user_purchase_item_next_page(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    check = db.check_user(call.from_user.id)
    get_category = db.get_category(category_id=category_id)

    if check == 'ru':
        await call.message.edit_text(f"<b>🎁 Текущая категория: <code>{get_category['category_name']}</code></b>",
                                     reply_markup=inline_page.item_swipe_fp(remover, category_id, check))
        await call.message.edit_text(f"<b>🎁 קטגוריה נוכחית: <code>{get_category['category_name']}</code></b>",
                                     reply_markup=inline_page.item_swipe_fp(remover, category_id, check))


###############################################################
############ Сама покупка #####################################

@dp.callback_query_handler(text_startswith="buy_item_open_finl:", state="*")
async def user_purchase_select(call: CallbackQuery, state: FSMContext):
    item_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    check = db.check_user(call.from_user.id)
    get_item = db.get_item(item_id=item_id)
    price = int(get_item['item_price'])


    await state.update_data(cache_item_id=item_id)
    await state.set_state("item_count")

    async with state.proxy() as data:
        data['price'] = price
        data['remover'] = remover
    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    if check == 'ru':
        await call.message.answer(ded(f"""
                                  <b>🎁 Введите количество товаров для покупки</b>
                                  ➖➖➖➖➖➖➖➖➖➖
                                  🎁 Товар: <code>{get_item['item_name']}</code> - <code>{price}₪</code>
                                  """))
    else:
        await call.message.answer(ded(f"""
                                  <b>🎁 הזן את מספר הפריטים לקנייה</b>
                                  ➖➖➖➖➖➖➖➖➖➖
                                  🎁 מוצר: <code>{get_item['item_name']}</code> - <code>{price}₪</code>
                                  """))

@dp.message_handler( state="item_count")
async def user_shop(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    try:
        if int(message.text) <= 0:
            await message.answer("ДОЛБАЕБ, ТЕБЯ ПРОСИЛИ БЛЯТЬ ВВЕСТИ КОЛИЧЕСТВА ТОВАРА, КАКОЕ НАХУЙ 0 ЕБАНАТ?")
        else:
            await message.answer("Ладно, красавчик")
    except ValueError:
        await message.answer("ДОЛБАЕБ, ТЕБЯ ПРОСИЛИ БЛЯТЬ ВВЕСТИ КОЛИЧЕСТВА ТОВАРА, КАКОЙ НАХУЙ ТЕКСТ ДЯДЕЛ?")


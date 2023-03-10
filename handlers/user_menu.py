# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageCantBeDeleted
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from modules.services import db, json_logic
from bot_telegram import dp
from modules.keyboards import inline_user, reply_user, inline_page
from handlers import start_user
from contextlib import suppress
from modules.utils.const_func import ded
from modules import alerts

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


    data = db.get_discout(item_id)
    if data['discount_len_item'] == None and data['discount'] == None:
        description_discount = ''
    else:
        if check == 'ru':
            description_discount = f"На этот товар действует скидка <code>{data['discount']}%</code> при заказе от <code>{data['discount_len_item']}шт.</code>"
        else:
            description_discount = f"מוצר זה מוזל ב- <code>{data['discount']}%</code> בהזמנה מ-<code>{data['discount_len_item']}pcs</code>"



    if get_item['item_description'] == "0":
        text_description = ""
    else:
        if check == 'ru':
            text_description = f"\n📜 Описание:\n{get_item['item_description']}"
        else:
            text_description = f"\n📜 תיאור:\n{get_item['item_description']}"

    if check == 'ru':
        send_msg = ded(f"""
                   <b>🎁 Покупка товара:</b>
                   ➖➖➖➖➖➖➖➖➖➖
                   🏷 Название: <code>{get_item['item_name']}</code>
                   🗃 Категория: <code>{get_category['category_name']}</code>
                   💰 Стоимость: <code>{get_item['item_price']}₪</code>
                   {text_description}
                   {description_discount}
                   """)
    else:
        send_msg = (
                    f"<b>🎁 רכישת מוצר:</b>\n"
                    f"➖➖➖➖➖➖➖➖➖➖\n"
                    f"🏷 שם: <code>{get_item['item_name']}</code>\n"
                    f"🗃 קטגוריה: <code> {get_category['category_name']}</code>\n"
                    f"💰 עלות: <code>{get_item['item_price']}₪</code>\n"
                    f"{text_description}"
                    f"{description_discount}"
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
        data['item_name'] = get_item['item_name']
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
            if check == 'ru':
                await message.answer("<b>Введите положительное число, которое не равно нулю</b>")
            else:
                await message.answer("<b>הזן מספר חיובי שאינו אפס< / b>")
        else:
            async with state.proxy() as data:
                item_id = data['cache_item_id']
                price = data['price']
                item_name = data['item_name']

            data = db.get_discout(item_id)
            price = price
            try:
                if  int(message.text) >= int(data['discount_len_item']):
                    price = price - (price / 100 * int(data['discount']))
            except TypeError:
                pass
            price = price * int(message.text)
            await state.set_state("item_buy")
            await state.update_data(len_item = int(message.text))
            if check == 'ru':
                await message.answer(ded(f"""
                                          <b>Вы подтверждаете покупку</b>
                                          ➖➖➖➖➖➖➖➖➖➖
                                          🎁 Название: <code>{item_name}</code>
                                          📦 Количество: <code>{int(message.text)}шт.</code> 
                                          💵 Стоимость:  <code>{price}₪</code> 
                                            """), reply_markup = inline_user.buy_item(check))

            else:
                await message.answer(ded(f"""
                                          <b>אתה מאשר את הרכישה</b>
                                          ➖➖➖➖➖➖➖➖➖➖
                                          🎁 שם: <code>{item_name}</code>
                                          📦 כמות: <code>{int(message.text)}pcs</code>
                                          💵 עלות: <code>{price}₪</code>
                                            """), reply_markup = inline_user.buy_item(check))

    except ValueError:
        if check == 'ru':
            await message.answer("<b>Введите число!</b>")
        else:
            await message.answer("< b>הזן מספר!</b>")

@dp.callback_query_handler(text_startswith="buy_item_final:", state="item_buy")
async def user_buy_item(call: CallbackQuery, state: FSMContext):
    selected = call.data.split(":")[1]
    check = db.check_user(call.from_user.id)
    if selected == 'yes':
        async with state.proxy() as data:
            item_name = data['item_name']
            price = data['price']
            len_item = data['len_item']

        if check == 'ru':
            await call.message.answer(ded(f"""
                                      <b>🎉 Вы купили товар, скоро с вами свяжется Администатор</b>
                                      ➖➖➖➖➖➖➖➖➖➖
                                      🎁 Название: <code>{item_name}</code>
                                      📦 Количество: <code>{len_item}шт.</code> 
                                      💵 Стоимость:  <code>{price}₪</code> 
                                        """),  reply_markup = reply_user.menu(call.from_user.id))
        else:
            await call.message.answer(ded(f"""
                                      <b>🎉 קנית מוצר, מנהל המערכת ייצור איתך קשר בקרוב</b>
                                      ➖➖➖➖➖➖➖➖➖➖
                                     🎁 שם: <code> {item_name}</code>
                                      📦 כמות: <code>{len_item}pcs</code>
                                      💵 עלות: <code>{price}₪</code>
                                        """), reply_markup = reply_user.menu(call.from_user.id))

        await alerts.send_admins(ded(f"""
                                      <b>Куплен товар!</b>
                                      ➖➖➖➖➖➖➖➖➖➖
                                      🎁 Название: <code>{item_name}</code>
                                      📦 Количество: <code>{len_item}шт.</code> 
                                      💵 Стоимость:  <code>{price}₪</code>
                                      👤 Пользователь: <b>@{call.from_user.username}</b>
                                        """))
    else:
        await start_user.user_menu(call.message, check)

@dp.message_handler(text = ['🏠 Наш канал', '🏠 הערוץ שלנו'], state = "*")
async def mychannel(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    if check == 'ru':
        message_text = json_logic.get_texts("mychannel_ru")
    else:
        message_text = json_logic.get_texts("mychannel_il")
    await message.answer(message_text)



@dp.message_handler(text = ['☎ Поддержка', '☎ תמיכה'], state = "*")
async def support(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    if check == 'ru':
        message_text = json_logic.get_texts("support_ru")
    else:
        message_text = json_logic.get_texts("support_il")
    await message.answer(message_text)



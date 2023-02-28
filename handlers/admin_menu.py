# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageCantBeDeleted
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from modules.services import db, json_logic
from bot_telegram import dp
from modules.keyboards import  reply_admin, inline_page, inline_user, inline_admin, reply_user
from contextlib import suppress
from modules.utils.check_func import CheckAdmin
from handlers import start_user
from bot_telegram import bot

@dp.message_handler(CheckAdmin(), text = ['🧑‍✈️ Администаторы', '🧑‍✈️ מנהלים'], state = "*")
async def admin_menu_start(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    if check == 'ru':
        await message.answer("<b>Панель управления администраторами</b>", reply_markup=reply_admin.admin__edit_selected(check))
    else:
        await message.answer("<b>לוח בקרה של מנהלים</b>", reply_markup=reply_admin.admin__edit_selected(check) )


@dp.message_handler(CheckAdmin(), text = ['Добавить Администратора', 'וסף מנהל'], state = "*")
async def admin_edit_menu(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    if check == 'ru':
        await message.answer("<b>Перешлите <code>сообщение пользователя</code>, которого хотите добавить в Администаторы, в диалог с ботом</b>", reply_markup=reply_admin.admin_back(check))
    else:
        await message.answer("<b>העבר את <code>ההודעה של המשתמש</code> שברצונך להוסיף למנהלי מערכת לתיבת הדו-שיח של הבוט</b>",  reply_markup=reply_admin.admin_back(check))
    await state.set_state("add_admin")

@dp.message_handler(CheckAdmin(), state = "add_admin")
async def add_admin(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    if message.text in ['Назад', 'חזור']:
        await state.finish()
        if check == 'ru':
            await message.answer("<b>Панель управления администраторами</b>", reply_markup=reply_admin.admin__edit_selected(check))
        else:
            await message.answer("<b>לוח בקרה של מנהלים</b>", reply_markup=reply_admin.admin__edit_selected(check) )
    else:
        try:
            user_id = message['forward_from']['id']
            if message['forward_from']['last_name'] == None:
                nickname = message['forward_from']['first_name']
            else:
                nickname = f"{message['forward_from']['first_name']} {message['forward_from']['last_name']}"

            result = json_logic.add_admin(user_id, nickname)
            if result:
                if check == 'ru':
                    await message.answer("<b>Успешно 👍</b>\n"
                                         f"Пользователь <code>{nickname}</code> добавлен в Администраторы",
                                         reply_markup=reply_admin.admin__edit_selected(check))
                else:
                    await message.answer("<b>בהצלחה 👍</b>\n"
                                         f"המשתמש <code>{nickname}</code> נוסף למנהלי מערכת",
                                         reply_markup=reply_admin.admin__edit_selected(check))
                await state.finish()

        except TypeError:
            if check == 'ru':
                await message.answer("<b>Не найдено пересланое сообщение. Повторите попытку! Или пользователь запретил пересылку сообщений</b>", reply_markup=reply_admin.admin_back(check))
            else:
                await message.answer("<b>הודעה שהועברה לא נמצאה. נסה שוב! או שהמשתמש השבית את העברת ההודעות</b>",  reply_markup=reply_admin.admin_back(check))
            await state.set_state("add_admin")

@dp.message_handler(CheckAdmin(), text = ['Удалить Администратора', 'הסר את מנהל המערכת'], state = "*")
async def admin_delete_admin(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    await see_admin(message, check)
    if check == 'ru':
        await message.answer("<b>Введите <code>ID Администратора</code>, которого хотите удалить 👆</b>", reply_markup=reply_admin.admin_back(check))
    else:
        await message.answer("<b>הזן את <code>מזהה המנהל</code> שברצונך להסיר 👆</b>", reply_markup=reply_admin.admin_back(check))
    await state.set_state("delete_admin")

@dp.message_handler(CheckAdmin(), text = ['חזרה לתפריט', 'Назад в меню'], state = "*")
async def admin_exit_menu(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    await start_user.user_menu(message, check)


@dp.message_handler(CheckAdmin(), state = "delete_admin")
async def admin_delete_admin(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    if message.text in ['Назад', 'חזור']:
        await state.finish()
        if check == 'ru':
            await message.answer("<b>Панель управления администраторами</b>", reply_markup=reply_admin.admin__edit_selected(check))
        else:
            await message.answer("<b>לוח בקרה של מנהלים</b>", reply_markup=reply_admin.admin__edit_selected(check) )
    else:
        admins = json_logic.see_admins()
        user_ids = []
        for character in admins:
            user_ids.append(character['user_id'])
        try:
            if int(message.text) in user_ids:
                json_logic.remove_admin(message.text)
                if check == 'ru':
                    await message.answer("<b>Успешно 👍</b>", reply_markup=reply_admin.admin__edit_selected(check))
                else:
                    await message.answer("<b>בהצלחה 👍</b>", reply_markup=reply_admin.admin__edit_selected(check))
                await state.finish()

            else:
                if check == 'ru':
                    await message.answer("<b>ID сообщения не найден! Повторите попытку</b>", reply_markup=reply_admin.admin_back(check))
                else:
                    await message.answer("<b>מזהה הודעה לא נמצא! אנא נסה שוב</b>", reply_markup=reply_admin.admin_back(check))
                await state.set_state("delete_admin")
        except ValueError:
            if check == 'ru':
                await message.answer("<b>ID сообщения должен содержать только целые числа. Повторите попытку</b>",reply_markup=reply_admin.admin_back(check))
            else:
                await message.answer("<b>מזהה ההודעה חייב להכיל מספרים שלמים בלבד. אנא נסה שוב</b>", reply_markup=reply_admin.admin_back(check))
            await state.set_state("delete_admin")


@dp.message_handler(CheckAdmin(), text = ['Посмотреть список Администраторов', 'הצג את רשימת המנהלים'], state = "*")
async def admin_see_admins(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    await see_admin(message, check)

async def see_admin(message, check):
    admins = json_logic.see_admins()
    text = ''
    if admins:
        for character in admins:
            text += f"<b>#{character['position']}  {character['nickname']} || <code>{character['user_id']}</code></b>\n"
    if check == 'ru':
        await message.answer(f"<b>ИМЯ ➖➖➖➖➖➖ ID</b>\n{text}")
    else:
        await message.answer(f"<b>שֵׁם ➖➖➖➖➖➖ ID</b>\n{text}")


@dp.message_handler(text = ['💲 Установление скидки', '💲 קביעת הנחה'], state = "*")
async def get_discout(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    if len(db.get_all_info('category')) >= 1:
        if check == 'ru':
            await message.answer("<b>🎁 Выберите категорию товара:</b>", reply_markup=inline_page.item_category_swipe_fp_discount(0, check))
        else:
            await message.answer("<b>🎁 בחר קטגוריית מוצרים:</b>",  reply_markup=inline_page.item_category_swipe_fp_discount(0, check))
    else:
        if check == 'ru':
            await message.answer("<b>🎁 Увы, товары в данное время отсутствуют.</b>")
        else:
            await message.answer("<b>🎁 אבוי, כרגע אין מוצרים.</b>")


#Следующая страница выбора категории
@dp.callback_query_handler(text_startswith="buy_category_swipe_discout:", state="*")
async def user_category_next_page_discout(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    check = db.check_user(call.from_user.id)
    if check == 'ru':
        await call.message.edit_text("<b>🎁 Выберите категорию товара:</b>", reply_markup=inline_page.item_category_swipe_fp_discount(remover, check))
    else:
        await call.message.edit_text("<b>🎁 בחר קטגוריית מוצרים:</b>", reply_markup=inline_page.item_category_swipe_fp_discount(remover, check))

@dp.callback_query_handler(text_startswith="buy_category_open_discout:", state="*")
async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    check = db.check_user(call.from_user.id)

    get_category = db.get_category(category_id=category_id)
    get_item = db.get_item(category_id=category_id)
    try:
        count = len(get_item)
    except TypeError:
        count = 0
    if count >= 1:
        with suppress(MessageCantBeDeleted):
            await call.message.delete()
        if check == 'ru':
            await call.message.answer(f"<b>🎁 Текущая категория: <code>{get_category['category_name']}</code></b>", reply_markup=inline_page.item_swipe_fp_discout(remover, category_id, check))
        else:
            await call.message.answer(f"<b>🎁 קטגוריה נוכחית: <code>{get_category['category_name']}</code></b>", reply_markup=inline_page.item_swipe_fp_discout(remover, category_id, check))
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

@dp.callback_query_handler(text_startswith="buy_item_open_discout:", state="*")
async def user_discout_get(call: CallbackQuery, state: FSMContext):
    item_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    check = db.check_user(call.from_user.id)
    get_item = db.get_item(item_id=item_id)
    get_category = db.get_category(category_id=category_id)

    await state.update_data(cache_item_id = item_id)
    await state.update_data(cache_category_id = category_id)
    await state.update_data(cache_remover  = remover)
    await state.set_state("get_len_items")
    if check == 'ru':
        await call.message.edit_text("<b>От какого количества товара должна начинаться скидка? 📦</b>", reply_markup=inline_user.get_discount(item_id, category_id, remover, check))
    else:
        await call.message.edit_text("<b > מאיזה כמות של מוצר צריך להתחיל הנחה? 📦</b>",   reply_markup=inline_user.get_discount(item_id, category_id, remover, check))

@dp.message_handler(state="get_len_items")
async def get_discount(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    await state.update_data(cache_len_items=message.text)
    async with state.proxy() as data:
        item_id = data['cache_item_id']
        category_id = data['cache_category_id']
        remover = data['cache_remover']
    try:
        if int(message.text) <= 0:
            if check == 'ru':
                await message.answer("<b>Введите положительное число, которое не равно нулю</b>", reply_markup=inline_user.get_discount(item_id, category_id, remover, check))
            else:
                await message.answer("<b>הזן מספר חיובי שאינו אפס< / b>", reply_markup=inline_user.get_discount(item_id, category_id, remover, check))
        else:
            await state.set_state("get_discout")
            if check == 'ru':
                await message.answer("<b>Введите  процент скидки</b>", reply_markup=inline_user.get_discount(item_id, category_id, remover, check))
            else:
                await message.answer("< b>הזן אחוז הנחה< / b>", reply_markup=inline_user.get_discount(item_id, category_id, remover, check))
    except ValueError:
        if check == 'ru':
            await message.answer("<b>Введите число!</b>",reply_markup=inline_user.get_discount(item_id, category_id, remover, check))
        else:
            await message.answer("< b>הזן מספר!</b>", reply_markup=inline_user.get_discount(item_id, category_id, remover, check))

@dp.message_handler(state="get_discout")
async def get_discount(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    async with state.proxy() as data:
        item_id = data['cache_item_id']
        len_items = data['cache_len_items']
    try:
        if int(message.text) <= 0:
            if check == 'ru':
                await message.answer("<b>Введите положительное число, которое не равно нулю</b>")
            else:
                await message.answer("<b>הזן מספר חיובי שאינו אפס< / b>")
        else:
            db.add_discout(int(message.text), len_items, item_id)
            await message.answer("Успешно!")

    except ValueError:
        if check == 'ru':
            await message.answer("<b>Введите число!</b>")
        else:
            await message.answer("< b>הזן מספר!</b>")


@dp.message_handler(text = ['⚒ ערוך טקסט', '⚒ Редактировать текста'], state = "*")
async def edit_texts(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    await state.set_state("change_texts")
    if check == 'ru':
        await message.answer("<b>⚒ Выберите нужный пункт:</b>", reply_markup=reply_admin.admin__edit_texts(check))
    else:
        await message.answer("<b>⚒ בחר את הפריט הרצוי:</b>",  reply_markup=reply_admin.admin__edit_texts(check))

@dp.message_handler(state = "change_texts")
async def edit_texts_selected(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    if message.text == 'Отмена' or message.text ==  'לְבַטֵל':
        await state.finish()
        await start_user.user_menu(message, check)
    else:
        if message.text in ["הערוץ שלנו", "תמיכה", "Поддержка", "Наш канал"]:
            if check == 'ru':
                await message.answer("<b>🇷🇺 🇮🇱 Выберите язык, текст которого будете изменять</b>", reply_markup = inline_admin.change_texts(message.text))
            else:
                await message.answer("<b>🇬🇧 🇮🇱 בחר את השפה שברצונך לשנות טקסט</b>",  reply_markup = inline_admin.change_texts(message.text))

@dp.callback_query_handler(text_startswith="change_text:", state="*")
async def change_texts_lang(call: CallbackQuery, state: FSMContext):
    lang = call.data.split(":")[1]
    text_category = call.data.split(":")[2]

    check = db.check_user(call.from_user.id)
    await state.set_state("change_text_final")

    if text_category == "Поддержка" or text_category == "תמיכה":
        message_text = json_logic.get_texts(f"support_{lang}")
        await state.update_data(text_category=f"support_{lang}")

    elif text_category == "Наш канал" or text_category == "הערוץ שלנו":
        message_text = json_logic.get_texts(f"mychannel_{lang}")
        await state.update_data(text_category= f"mychannel_{lang}")

    with suppress(MessageCantBeDeleted):
        await call.message.delete()


    async with state.proxy() as data:
        data['lang'] = lang
    if check == 'ru':
        await call.message.answer(f"<b>Введите новый текст данного отдела!</b>\nСтарый текст таков: \n\n<i>{message_text}</i>", reply_markup = reply_admin.admin__edit_texts_cancel(check))
    else:
        await call.message.answer( f"<b>הזן את הטקסט החדש עבור המחלקה הזו!</b>\nהטקסט הישן הוא: \n\n<i>{message_text}</i>", reply_markup = reply_admin.admin__edit_texts_cancel(check))


@dp.message_handler(state = "change_text_final")
async def edit_texts_selected(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    if message.text == 'Отмена' or message.text ==  'לְבַטֵל':
        await state.finish()
        await start_user.user_menu(message, check)
    else:
        async with state.proxy() as data:
            text_category = data['text_category']
        json_logic.update_texts(text_category, message.text)
        await state.finish()
        if check == 'ru':
            await message.answer("Успешно!", reply_markup = reply_user.menu(message.from_user.id))
        else:
            await message.answer("בְּהַצלָחָה!", reply_markup=reply_user.menu(message.from_user.id))


@dp.message_handler(text = ['🛎 Рассылка', '🛎 ניוזלטר'], state = "*")
async def alerts_start(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    await state.set_state("alerts_users")
    if check == 'ru':
        await message.answer("<b>Введите <code>сообщение</code> для рассылки пользователям</b>\n\n<i>Также вы можете обратиться к пользователям по имени, для этого вставьте конструкцию <code>{username}</code>.</i>", reply_markup=reply_admin.admin__edit_texts_cancel(check))
    else:
        await message.answer("<b>הזן <code>הודעה</code> כדי לשלוח למשתמשים</b>\n\n<i>תוכל גם לפנות למשתמשים לפי שם, לשם כך, הכנס את המבנה <code>{שם משתמש}</ קוד>. </i>", reply_markup=reply_admin.admin__edit_texts_cancel(check))


@dp.message_handler(state = "alerts_users")
async def alerts_confirm(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    users = db.get_users()

    if message.text == 'Отмена' or message.text ==  'לְבַטֵל':
        await state.finish()
        await start_user.user_menu(message, check)
    else:
        await state.set_state("alerts_finish")
        await state.update_data(message_text = message.text)
        await state.update_data(users = users)
        if check == 'ru':
            await message.answer(f"<b>Вы уверены, что хотите сделать рассылку <code>{len(users)}</code> пользователям</b>\n\n<i>{message.text}</i>", reply_markup=inline_admin.alerts_confirm())
        else:
            await message.answer(f"<b>האם אתה בטוח שברצונך לשלוח <code>{len(users)}</code> למשתמשים</b>\n\n<i>{message.text}</i>", reply_markup=inline_admin.alerts_confirm())



@dp.callback_query_handler(text_startswith="alerts_confirm:", state="alerts_finish")
async def alerts_finish(call: CallbackQuery, state: FSMContext):
    selected = call.data.split(":")[1]
    check = db.check_user(call.from_user.id)
    if selected == 'yes':
        async with state.proxy() as data:
            users = data['users']
            message_text = data['message_text']
        for i in users:
            try:
                await bot.send_message(i['user_id'], message_text.format(username = i['username']) )
            except:
                pass
        await state.finish()
        if check == 'ru':
            await call.message.answer("<b>Успешно!</b>", reply_markup = reply_user.menu((call.from_user.id)))
        else:
            await call.message.answer("<b>הצלחה!</b>", reply_markup = reply_user.menu((call.from_user.id)))
    else:
        await start_user.user_menu(call.message, check)
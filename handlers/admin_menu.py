# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageCantBeDeleted
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from modules.services import db, json_logic
from bot_telegram import dp
from modules.keyboards import  reply_admin
from contextlib import suppress
from modules.utils.check_func import CheckAdmin
from handlers import start_user
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
        admins = await json_logic.see_admins()
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



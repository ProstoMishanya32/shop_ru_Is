# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageCantBeDeleted
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from modules.services import db
from bot_telegram import dp
from modules.keyboards import inline_user, reply_user
from contextlib import suppress

@dp.message_handler(text = ['/start'], state = "*")
async def start(message: Message, state: FSMContext):
    await state.finish()
    check = db.check_user(message.from_user.id)
    if check:
        await user_menu(message, check)
    else:
        await message.answer("<b>Выберите язык 🇷🇺\n"
                             "➖➖➖➖➖➖\n"
                             " 🇮🇱 בחר שפה </b>", reply_markup=inline_user.select_lang())


async def user_menu(message, check):
    if check == 'ru':
        await message.answer("<b>➖➖➖Добро пожаловать в меню 🏠➖➖➖</b>\n\n"
                             "🔶 Если не появились вспомогательные кнопки\n"
                             "▶️ Введите /start", reply_markup=reply_user.menu((message.from_user.id)))
    else:
        await message.answer("<b>➖➖➖ברוכים הבאים לתפריט 🏠➖➖➖</b>\n\n"
                             "🔶 אם לחצני עזר לא מופיעים\n"
                             "▶️ הקלד / התחל", reply_markup=reply_user.menu((message.from_user.id)))





@dp.callback_query_handler(text_startswith="select_lang:", state="*")
async def user_selected_lang(call: CallbackQuery, state: FSMContext):
    await state.finish()
    select = call.data.split(":")[1]
    db.registation_user(call.from_user.id, call.from_user.username, select)
    with suppress(MessageCantBeDeleted):
        await call.message.delete()
    if select == "ru":
        await call.answer("Успешно")
        await call.message.answer("<b>➖➖➖Добро пожаловать в меню 🏠➖➖➖</b>\n\n"
                             "🔶 Если не появились вспомогательные кнопки\n"
                             "▶️ Введите /start", reply_markup=reply_user.menu((call.from_user.id)))
    else:
        await call.message.answer("<b>➖➖➖ברוכים הבאים לתפריט 🏠➖➖➖</b>\n\n"
                             "🔶 אם לחצני עזר לא מופיעים\n"
                             "▶️ הקלד / התחל", reply_markup=reply_user.menu((call.from_user.id)))




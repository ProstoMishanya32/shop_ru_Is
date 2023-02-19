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


@dp.message_handler(text = ['🇮🇱 Сменить язык 🇷🇺', '🇮🇱 שנה שפה 🇷🇺', '/changelang'], state = "*")
async def change_select(message: Message, state: FSMContext):
    await message.answer("<b>Выберите язык 🇷🇺\n"
                         "➖➖➖➖➖➖\n"
                         " 🇮🇱 בחר שפה </b>", reply_markup=inline_user.select_lang())



@dp.message_handler(text = ['🎁 Каталог', '🎁 קטלוג'], state="*")
async def user_shop(message: Message, state: FSMContext):
    await state.finish()

    if len(db.get_all_info('category')) >= 1:
        await message.answer("<b>🎁 Выберите нужный вам товар:</b>",  reply_markup=inline_page.item_category_swipe_fp(0))
    else:
        await message.answer("<b>🎁 Увы, товары в данное время отсутствуют.</b>")

#Страницы позиций для покупки товаров
def products_item_position_swipe_fp(remover, category_id):
    items = db.get_category(category_id=category_id)
    keyboard = InlineKeyboardMarkup()

    if remover >= len(items): remover -= 10

    for count, a in enumerate(range(remover, len(items))):
        if count < 10:
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {items[a]['position_price']}₽ | шт",
                callback_data=f"buy_position_open:{items[a]['position_id']}:{category_id}:{remover}"))

    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_position_swipe:{category_id}:{remover + 10}"),
        )
    elif remover + 10 >= len(get_positions):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_position_swipe:{category_id}:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_position_swipe:{category_id}:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_position_swipe:{category_id}:{remover + 10}"),
        )
    keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_category_swipe:0"))

    return keyboard

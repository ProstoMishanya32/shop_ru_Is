# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from modules.utils import main_config
from modules.services import json_logic

class CheckAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if message.from_user.id in json_logic.get_admins() or message.from_user.id == main_config.bot.main_admin:
            return True
        else:
            return False
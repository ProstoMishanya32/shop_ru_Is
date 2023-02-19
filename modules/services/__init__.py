from . import sqlite_logic
from modules.utils import main_config


db = sqlite_logic.DataBase(main_config.dabases.main_db)
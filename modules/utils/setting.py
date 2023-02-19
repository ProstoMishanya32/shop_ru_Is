from modules.utils.creater_config import CreatingConfig



class MainConfig(CreatingConfig):
    def __init__(self) -> None:
        super().__init__(path = 'data/main_config.json')
        self.bot = self.Bot(config = self)
        self.logs = self.Logs(config = self)
        self.dabases = self.Dabases(config = self)
    class Bot:
        def __init__(self, config : CreatingConfig) -> None:
            self.token = config.config_field(key = 'token', layer = 'bot', default = 'Здесь ваш Telegram Токен')
            self.main_admin = config.config_field(key='main_admin', layer='bot', default='Самый главный Администатор')
            self.admins = config.config_field(key = 'admins', layer = 'bot', default = [])
    class Logs:
        def __init__(self, config : CreatingConfig) -> None:
            self.main_path_logs = config.config_field(key = 'main_path_logs', layer = 'logs', default = 'Путь к папке логов')
    class Dabases:
        def __init__(self, config : CreatingConfig) -> None:
            self.main_db = config.config_field(key = 'main_db', layer = 'main_db', default = 'Путь и имя  основной Базы данных')
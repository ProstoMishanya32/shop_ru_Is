# - *- coding: utf- 8 - *-
import colorlog
from modules.utils import main_config
import logging as logger

# Формат логгирования
log_formatter_file = logger.Formatter("%(levelname)s | %(asctime)s | %(filename)s:%(lineno)d | %(message)s")
log_formatter_console = colorlog.ColoredFormatter(
    "%(purple)s%(levelname)s %(blue)s|%(purple)s %(asctime)s %(blue)s|%(purple)s %(filename)s:%(lineno)d %(blue)s|%(purple)s %(message)s%(red)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)


# Логгирование в файл /data/logs.log
file_logging = logger.FileHandler(main_config.logs.main_path_logs, "w", "utf-8")
file_logging.setFormatter(log_formatter_file)
file_logging.setLevel(logger.INFO)

# Логгирование в консоль
console_logging = logger.StreamHandler()
console_logging.setFormatter(log_formatter_console)
console_logging.setLevel(logger.CRITICAL)


logger.basicConfig(
    format="%(levelname)s | %(asctime)s | %(filename)s:%(lineno)d | %(message)s",
    handlers=[file_logging, console_logging]
)

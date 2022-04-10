"""Конфиг клиентского логирования """

import sys
import os
import logging

# from pprint import pprint
from common.variables import LOGGING_LEVEL
sys.path.append('../')
# pprint(sys.path)


# создаём формировщик логов (formatter):
CLIENT_FORMATTER = logging.Formatter("%(asctime)s %(levelno)s %(levelname)s %(module)s %(message)s")

# Подготовка имени файла для логирования.
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

# создаём потоки вывода логов
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE = logging.FileHandler(PATH, encoding='utf8')
LOG_FILE.setFormatter(CLIENT_FORMATTER)

# создаём регистратор и настраиваем его
LOGGER = logging.getLogger('client')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.warning('Предупреждение')
    LOGGER.info('Информационное сообщение')
    LOGGER.debug('Отладочная информация')

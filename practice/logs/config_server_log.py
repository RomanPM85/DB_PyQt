"""Конфиг клиентского логирования """

import sys
import os
import logging
import logging.handlers

# from pprint import pprint
from common.variables import LOGGING_LEVEL
sys.path.append('../')
# pprint(sys.path)

# создаём формировщик логов (formatter):
SERVER_FORMATTER = logging.Formatter('%(asctime)s %(levelno)s %(levelname)s %(module)s %(message)s')

# Подготовка имени файла для логирования.
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

# создаём потоки вывода логов
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
LOG_FILE.setFormatter(SERVER_FORMATTER)

# создаём регистратор и настраиваем его
logging = logging.getLogger('server')
logging.addHandler(STREAM_HANDLER)
logging.addHandler(LOG_FILE)
logging.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    logging.critical('Критическая ошибка')
    logging.error('Ошибка')
    logging.warning('Предупреждение')
    logging.info('Информационное сообщение')
    logging.debug('Отладочная информация')

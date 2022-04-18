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
server_formatter = logging.Formatter('%(asctime)s %(levelno)s %(levelname)s %(module)s %(message)s')

# Подготовка имени файла для логирования.
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'server.log')

# создаём потоки вывода логов
steam = logging.StreamHandler(sys.stderr)
steam.setFormatter(server_formatter)
steam.setLevel(logging.INFO)
log_file = logging.handlers.TimedRotatingFileHandler(path, encoding='utf8', interval=1, when='D')
log_file.setFormatter(server_formatter)

# создаём регистратор и настраиваем его
logger = logging.getLogger('server_dist')
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    logging.critical('Критическая ошибка')
    logging.error('Ошибка')
    logging.warning('Предупреждение')
    logging.info('Информационное сообщение')
    logging.debug('Отладочная информация')

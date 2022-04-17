"""Декораторы"""

import sys
import logging
import logs.config_server_log
import logs.config_client_log

# метод определения модуля, источника запуска.
if sys.argv[0].find('client_dist') == -1:
    # если не клиент, то сервер!
    logger = logging.getLogger('server_dist')
else:
    # если не сервер, то клиент
    logger = logging.getLogger('client_dist')


def log(func_to_log):
    """Функция декоратор"""
    def log_saver(*args, **kwargs):
        logger.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args} , {kwargs}. '
                     f'Вызов из модуля {func_to_log.__module__}')
        ret = func_to_log(*args, **kwargs)
        return ret
    return log_saver

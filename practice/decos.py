"""Декораторы"""

import sys
import logging
import logs.config_server_log
import logs.config_client_log
import traceback
import inspect

# Метод определения модуля, источника запуска.
# Метод find () возвращает индекс первого вхождения искомой подстроки,
# если он найден в данной строке.
# Если его не найдено, - возвращает -1.


def log(func_to_log):
    """Функция-декоратор"""
    def log_saver(*args, **kwargs):
        logger_name = 'server' if 'server.py' in sys.argv[0] else 'client'
        LOGGER = logging.getLogger(logger_name)

        ret = func_to_log(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}.'
                     f'Вызов из модуля {func_to_log.__module__}.'
                     f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     
                     # And two more options for determining the function from which the current function was called  
                     f'Вызов из функции {inspect.stack()[1][3]}'
                     
                     f'Вызов из функции {sys._getframe().f_back.f_code.co_name}'
                     f'вызов из модуля {sys._getframe().f_back.f_code.co_filename.split("/")[-1]}')
        return ret
    return log_saver

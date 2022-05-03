import logs.config_client_log
import logs.config_server_log
import socket
import logging
import sys
sys.path.append('../')


# метод определения модуля, источника запуска.
if sys.argv[0].find('client_dist') == -1:
    # если не клиент, то сервер!
    logger = logging.getLogger('server_dist')
else:
    # иначе сервер
    logger = logging.getLogger('client_dist')


def log(func_to_log):
    """Декоратор, выполняющий логирование вызовов функций.
    Сохраняет события типа debug, содержащие
    информацию об имени вызываемой функции, параметры с которыми
    вызывается функция, и модуль, вызывающий функцию.
    """

    def log_saver(*args, **kwargs):
        logger.debug(
            f'Была вызвана функция {func_to_log.__name__} c параметрами {args} , {kwargs}. '
            f'Вызов из модуля {func_to_log.__module__}')
        ret = func_to_log(*args, **kwargs)
        return ret

    return log_saver


def login_required(func):
    """Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    """

    def checker(*args, **kwargs):
        """Проверяем, что первый аргумент - экземпляр MessageProcessor
        Импорт необходим, иначе ошибка рекурсивного импорта.
        :param args:
        :param kwargs:
        :return:
        """
        from server.core import MessageProcessor
        from common.variables import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса
                    # MessageProcessor
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence
            # сообщение. Если presence, то разрешаем
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            # Если не авторизован и нет сообщение начала авторизации, тогда
            # вызываем исключение.
            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker

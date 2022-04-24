"""
В основе метода библиотека dis - анализ кода с помощью его дизассемблирования
(разбор кода на составляющие: в нашем случае - на атрибуты и методы класса)
https://docs.python.org/3/library/dis.html
"""

import dis


class ServerVerifier(type):
    """ Метакласс для проверки соответствия сервера: """
    def __init__(cls, clsname, bases, clsdict):
        methods = []
        """
        Список методов, которые используются в функциях класса:
        """
        attrs = []
        """
        Атрибуты, вызываемые функциями классов.
        """
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
                """
                Если не функция то ловим исключение.
                """
            except TypeError:
                pass
            else:
                """
                Раз функция разбираем код, получая используемые методы и атрибуты.
                """
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
        if 'connect' in methods:
            raise TypeError('Использование метода connect недопустимо в серверном классе')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')
        super().__init__(clsname, bases, clsdict)


class ClientVerifier(type):
    """
    Метакласс для проверки корректности клиентов:
    """
    def __init__(cls, clsname, bases, clsdict):
        methods = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('В классе обнаружено использование запрещённого метода')
        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
        super().__init__(clsname, bases, clsdict)

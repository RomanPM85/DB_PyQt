"""
Geekbrains_DB_PyQt

Task Lesson 1
1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
 Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с
помощью функции ip_address(). (Внимание! Аргументом субпроцесса должен быть список, а не строка!!! Крайне желательно
использование потоков.)
2. Написать функцию host_range_ping() (возможности которой основаны на функции из примера 1) для перебора ip-адресов
из заданного диапазона. Меняться должен только последний октет каждого адреса. По результатам проверки должно
выводиться соответствующее сообщение.
3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2. Но в данном случае
результат должен быть итоговым по всем ip-адресам, представленным в табличном формате (использовать модуль tabulate).
Таблица должна состоять из двух колонок и выглядеть примерно так:
Reachable

10.0.0.1
10.0.0.2
Unreachable

10.0.0.3
10.0.0.4
"""

import os
import platform
import subprocess
import threading
import time
from ipaddress import ip_address
from tabulate import tabulate


host_list = ['yandex.ru', 'google.com', 'gb.ru', '127.0.0.1']
output = {'Reachable': '', 'Unreachable': ''}
DNULL = open(os.devnull, 'w')


def check_is_ipaddress(value):
    try:
        ipv4 = ip_address(value)
    except ValueError:
        raise Exception('Некорректный ip')
    return ipv4


def host_ping(hosts_list=None, get_list=None):
    threads = []
    for host in hosts_list:
        try:
            ipv4 = check_is_ipaddress(host)
        except Exception as e:
            print(f'{host} - {e}')
            ipv4 = host
        thread = threading.Thread(target=ping, args=(ipv4, output, get_list), daemon=True)
        thread.start()
        threads.append(thread)

        for thread in threads:
            thread.join()

        if get_list:
            return output


def ping(ipv4, result, get_list):
    param = '-n' if platform.system().lower() == 'Linux' else '-c'
    response = subprocess.Popen(["ping", param, '1', '-w', '1', str(ipv4)], stdout=subprocess.PIPE)
    if response.wait() == 0:
        result["Reachable"] += f'{ipv4}\n'
        res = f'{ipv4} - Узел доступен'
        if not get_list:
            print(res)
        return res


def host_range_ping(get_list=False):
    while True:
        start_ip = input("Введите адрес: ")
        try:
            ipv4_start = check_is_ipaddress(start_ip)
            last_oct = int(start_ip.split('.')[3])
            break
        except Exception as e:
            print(e)
    while True:
        end_ip = input("Сколько адресов проверить?: ")
        if not end_ip.isnumeric():
            print("Ввести количество: ")
        else:
            if (last_oct + int(end_ip)) > 255+1:
                print(f'Можем менять последний октет, '
                      f'максимальное число хостов {255+1 - last_oct}')
            else:
                break

    [host_list.append(str(ipv4_start + x)) for x in range(int(end_ip))]
    if not get_list:
        host_ping(host_list)
    else:
        return host_ping(host_list, True)


def host_range_ping_tab():
    res_dict = host_range_ping(True)
    print(tabulate([res_dict], headers='keys', tablefmt='pipe', stralign='center'))


if __name__ == '__main__':
    start = time.time()
    host_ping(host_list)
    end = time.time()
    host_range_ping()
    host_range_ping_tab()

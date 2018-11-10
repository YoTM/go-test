#!/usr/bin/python3

import sys
import csv
import re


def prep_str(s):
    """
        ф-я заменяет в строке запятые между url-vb на "|"
    """
    return s.replace(',http', '|http')


def check_listing(val):
    """
        ф-я проверки строки на содержание нескольких url-ов
    """

    return val.find(',http', 0, len(val)) == -1


def check_ip(val):
    """
        ф-я проверка строки на соответствие IP-адресу
    """
    try:

        return re.search(r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$", val)
    except Exception as other:
        print("Ошибка проверки на IP...", val, other)


def check_url(url):
    """
        ф-я проверки валидности url-а
    """

    try:
        return re.search(r"http[s]?://(?:[a-zA-Z]|(?:[а-яА-Я])|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", url)
    except Exception as other:
        print("Ошибка проверки на url...", url, other)


def check_value(rlist, value, bads):
    """
        пр-ра проверки значений строки записи файла
        - проверка на перечисление url-ов
    """

    # если строка - это один url, то добавляем в список результатов
    if check_url(value) and check_listing(value):
        rlist.append([value])
    else:
        # подготавливаем строку с url-ми
        value = prep_str(value)
        # делим их по запятой и записываем в список
        values = value.split('|')
        # проверяем на валидность url-лы
        for v in values:
            if check_url(str(v)):
                rlist.append([v])
            else:
                # записываем отброшенные строки в список
                bads.append(v)


def csv_parser(file_obj):
    """
        Процедура обработки строк файла адресов
    """
    # читаем файл с данными
    data = csv.reader(file_obj, delimiter=';')
    # получаем список списков (строка файла данных = списку значений)
    data_list = [row for row in data]

    # Альтернативные регулярки:
    # проверка на url   /^(https?:\/\/)?([\w\.]+)\.([a-z]{2,6}\.?)(\/[\w\.]*)*\/?$/
    # проверка на URI ^(([ ^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?
    # проверка на IP    /^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$/

    # print('Парсинг данных начался...')

    urls_list = []  # список проверенных url-ов
    bad_value = []  # список отработки/мусора

    for item in data_list:
        # проверяем ячейку на наличие записи
        if item[1] != '':
            # проверяем запись на соответствие url-у
            check_value(urls_list, item[1], bad_value)
        # если в первой ячейке нет валидных url-ов, то добавляем в список результата домен из ячейки 2
        else:
            # если вместо домена не IP-ик и ячейка не пустая
            if not check_ip(item[2]) and item[2] != '':
                urls_list.append([item[2]])
            else:
                # если запись проверку не прошла, то добавляем строку в отработку
                bad_value.append(item[2])

    # print("Парсинг данных завершён...")
    # Вывод результата в консоль
    for line in urls_list:
        print('\n'.join(line))

    # with open("result.csv", "w") as file:
    #     writer = csv.writer(file, delimiter=';')
    #     for line in urls_list:
    #         writer.writerow(line)

    with open("bads.txt", "w") as file:
        print(*bad_value, file=file, sep="\n")

    # print("Результаты записаны...")


if __name__ == "__main__":

    csv_path = sys.stdin.read()    # "data.csv"     # sys.stdin.read()

    with open(csv_path, "r") as f_obj:
        csv_parser(f_obj)


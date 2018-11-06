#!/usr/bin/python3

import sys
import csv
import re


def check_value(rlist, value):
    """
        пр-ра проверки значений строки записи файла
        - проверка на перечисление url-ов
    """
    # если в ячейке записи url-лы перечисляются, т.е. их несколько
    if re.search(r"[\,]", value):
        # делим их по запятой и записываем в список
        values = value.split(',')
        for v in values:
            rlist.append([v])
    else:
        rlist.append([value])


def csv_parser(file_obj):
    """
        Процедура обработки строк файла адресов
    """
    # читаем файл с данными
    data = csv.reader(file_obj, delimiter=';')
    # получаем список списков (строка файла данных = списку значений)
    data_list = [row for row in data]

    # Обработка файла регулярками
    # проверка на url   /^(https?:\/\/)?([\w\.]+)\.([a-z]{2,6}\.?)(\/[\w\.]*)*\/?$/
    # проверка на IP    /^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$/

    print('Start parsing...')

    urls_list = []

    for item in data_list:

        if item[1] != '':
            check_value(urls_list, item[1])

        elif item[2] != '':
            urls_list.append([item[2]])

    print("Parsing complete...")

    with open("result.csv", "w") as file:
        writer = csv.writer(file, delimiter=';')
        for line in urls_list:
            writer.writerow(line)

    print("file output.csv is ready...")


if __name__ == "__main__":

    csv_path = "data.csv"     #sys.stdin.read()

    with open(csv_path, "r") as f_obj:
        csv_parser(f_obj)


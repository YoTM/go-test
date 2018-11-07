#!/usr/bin/python3

import sys
import csv
import re


def check_url(url):
    """
        ф-я проверки валидности url-а
    """

    try:
        return re.search(r"/^(https?:\/\/)?([\w\.]+)\.([a-z]{2,6}\.?)(\/[\w\.]*)*\/?$/", url)

    except Exception as other:
        print("Ошибка обработки url'а...", url)


def check_value(rlist, value):
    """
        пр-ра проверки значений строки записи файла
        - проверка на перечисление url-ов
    """
    bad_value = []

    if check_url(value):
        rlist.append([value])
    else:
        # делим их по запятой и записываем в список
        values = value.split(',')
        for v in values:
            if check_url(str(v)):
                rlist.append([v])
            else:
                bad_value.append(v)

    with open("bads.txt", "w") as file:
        print(bad_value, file=file, sep='\n')


    # если в ячейке записи url-лы перечисляются, т.е. их несколько
    # if re.search(r"[\,]", value):
    #     # делим их по запятой и записываем в список
    #     values = value.split(',')
    #     for v in values:
    #         rlist.append([v])
    # else:
    #     rlist.append([value])


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
            if check_url(item[2]):
                urls_list.append([item[2]])

    print("Parsing complete...")



    # print("Urls check complete...")

    with open("result.csv", "w") as file:
        writer = csv.writer(file, delimiter=';')
        for line in urls_list:
            writer.writerow(line)

    print("file output.csv is ready...")


if __name__ == "__main__":

    csv_path = "data.csv"     #sys.stdin.read()

    with open(csv_path, "r") as f_obj:
        csv_parser(f_obj)


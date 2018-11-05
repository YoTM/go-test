#!/usr/bin/python3

import sys
import csv
import re


def csv_parser(file_obj):
    """
        Процедура обработки строк файла адресов
    """
    data = csv.reader(file_obj, delimiter=';')
    # получаем список списков (строка файла данных = списку значений)
    data_list = [row for row in data]

    # Обработка файла регулярками /^(https?:\/\/)?([\w\.]+)\.([a-z]{2,6}\.?)(\/[\w\.]*)*\/?$/



    # Запись результата парсинга в файл

    # with open("output.txt", "w") as file:
        # for item in data_list:
        #     print(item, file=file)

    res_list = []


    for item in data_list:
        for val in item:
            # print(val)
            if re.search(r"[*]", val) or re.search(r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$", val):
                print(val)
                res_list.append(val)

    print("Parsing complete...")

    with open("result.csv", "w", newline='') as file:
        csv.writer(file).writerow(res_list)


if __name__ == "__main__":

    csv_path = "data.csv"     #sys.stdin.read()

    with open(csv_path, "r") as f_obj:
        csv_parser(f_obj)


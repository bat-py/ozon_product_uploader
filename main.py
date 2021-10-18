import csv
import os
from PIL import Image
from pyzbar.pyzbar import decode
from uploader import uploader
import socket

def get_header():
    """
    Из файла config.ini берет Client-Id и Api-Key. Вернет библиотеку header = {'Client-Id': data[0], 'Api-Key': data[1]}
    """

    with open('config.ini') as conf:
        config = conf.readlines()

        data = [i.split('=')[1].strip().replace('"', '') for i in config]
        header = {'Client-Id': data[0], 'Api-Key': data[1]}

        return header


def get_product_data():
    with open("positions.csv", encoding='utf-8') as r_file:
        items_csv = {}

        # Создаем объект reader, указываем символ-разделитель ","
        file_reader = csv.reader(r_file, delimiter=";")
        # Счетчик для подсчета количества строк и вывода заголовков столбцов
        count = 0
        # Считывание данных из CSV файла
        for row in file_reader:
            if count == 0:
                # Вывод строки, содержащей заголовки для столбцов
                print(f'Файл содержит столбцы: {", ".join(row)}')
            else:
                items_csv[row[3]] = row[1]

            count += 1
        return items_csv


def photos_handler(items_csv):
    """
    Вернет dict c данными:
    {'X120385-c01': ['fotos/Сеанс в студии-1116.jpg', 'fotos/Сеанс в студии-1117.jpg', ...], 'X8496-10-91': [...], ...}
    Ключ это артикул товара, а в массиве ссылки на фотографии товора

    :param items_csv:
    :return:
    """

    fotos = os.listdir('fotos')
    fotos.sort()

    hostname = socket. gethostname()
    local_ip = socket. gethostbyname(hostname)

    fotosart = {}
    group = []
    for foto in fotos:
        path = os.path.join('fotos', foto)
        img = Image.open(path)
        dec = decode(img)
        if not dec:
            group.append(os.path.join(local_ip, 'upload', foto))
        else:
            try:
                barcode = dec[0].data.decode()
                article = items_csv[barcode.replace('+', '').lower()]

                fotosart[article] = group
            finally:
                group = []

    print(fotosart)
    return fotosart

if __name__ == '__main__':
    header = get_header()

    product_data = get_product_data()

    photos_handler(product_data)
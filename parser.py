# Импортируем необходимые библиотеки
import os
from bs4 import BeautifulSoup
import requests
from icrawler.builtin import GoogleImageCrawler
from datetime import datetime
from PIL import Image

# Время старта выполнения программы
start_time = datetime.now()

# Создаём словарь с названиями грибов
mushrooms = {
    'edible': [],  # Съедобные
    'inedible': [],  # Несъедобные
    'poisonous': [],  # Ядовитые
    'hallucinogenic': []  # Галлюциногенные
}


# Функция для парсинга названий грибов
def parser_name(style, url):
    """
    :param style: к какому типу относятся грибы на сайте
    :param url: ссылка к сайту
    Программа получает на вход тип грибов и ссылку на сайт, с которого производится парсинг данных
    После выполнения функции создаётся папка с фотографиями грибов
    """
    r = requests.get(url)
    html = BeautifulSoup(r.content, 'html.parser')
    for el in html.select('.mush-block > a'):
        mushrooms[style].append(el.text)
    mushrooms[style] = list(set(mushrooms[style]))


# Парсим названия грибов
parser_name('edible', 'http://ya-gribnik.ru/syedobnye-griby.php')
parser_name('inedible', 'http://ya-gribnik.ru/nesyedobnye-griby.php')
parser_name('poisonous', 'http://ya-gribnik.ru/yadovitye-griby.php')
parser_name('hallucinogenic', 'http://ya-gribnik.ru/info/gallucinogennye-griby.php')
print('The name of the mushrooms is ready')


isdir = 'PATH'  # Путь к папке
dataset = {'Train': 16, 'Valid': 4, 'Test': 2}  # Распределение фото в датасете

# Цикл для создания директорий и скачивания фото
number_file = 1  # Счётчик фото
for sample, count in dataset.items():
    if not os.path.exists(f'{isdir}\\{sample}'):
        os.mkdir(f'{isdir}\\{sample}')
    for key in mushrooms.keys():
        for name in mushrooms[key]:
            if not os.path.exists(f'{isdir}\\{sample}\\{key}'):
                os.mkdir(f'{isdir}\\{sample}\\{key}')
            google_crawler = GoogleImageCrawler(
                storage={
                    'root_dir': f'{isdir}\\{sample}\\{key}'
                })
            # Переделать в функцию скачивания
            google_crawler.crawl(keyword=f'Гриб {name} фото',
                                 max_num=count,
                                 filters=dict(size='medium' if sample == 'Train' else 'large')
                                 )
            # Переименование фотографий
            for name_file in os.listdir(f'{isdir}\\{sample}\\{key}\\'):
                if name_file[0] != 'M':
                    os.rename(f'{isdir}\\{sample}\\{key}\\{name_file}',
                              f'{isdir}\\{sample}\\{key}\\M{str(number_file).rjust(6, "0")}'
                              f'.{name_file[len(name_file) - 3:]}')
                    number_file += 1
        number_file = 1

    # Скачивание фотографий не относящихся к грибам
    key = 'No'
    if not os.path.exists(f'{isdir}\\{sample}\\{key}'):
        os.mkdir(f'{isdir}\\{sample}\\{key}')
    no_mushrooms = ['человек', 'стол', 'блюдо']
    for name_photo in no_mushrooms:
        google_crawler = GoogleImageCrawler(
            storage={
                'root_dir': f'{isdir}\\{sample}\\{key}'
            })
        google_crawler.crawl(keyword=f'Фото {name_photo}',
                             max_num=count,
                             filters=dict(size='medium' if sample == 'Train' else 'large')
                             )
        # Переименовывание фото
        for name_file in os.listdir(f'{isdir}\\{sample}\\{key}\\'):
            if name_file[0] != 'M':
                os.rename(f'{isdir}\\{sample}\\{key}\\{name_file}',
                          f'{isdir}\\{sample}\\{key}\\M{str(number_file).rjust(6, "0")}'
                          f'.{name_file[len(name_file) - 3:]}')
                number_file += 1
    number_file = 1

# Изменение размерности изображения
key = 'No'
for sample, _ in dataset.items():
    for key in os.listdir(f'{isdir}\\{sample}'):
        for name_file in os.listdir(f'{isdir}\\{sample}\\{key}'):
            img = Image.open(f'{isdir}\\{sample}\\{key}\\{name_file}')
            new_image = img.resize((224, 224))
            new_image = new_image.convert('RGB')
            new_image.save(f'{isdir}\\{sample}\\{key}\\{name_file}')
        print(f'The {sample}\\{key} folder has been processed')

# Общее время работы программы
print(f'Program execution time: {datetime.now() - start_time}')

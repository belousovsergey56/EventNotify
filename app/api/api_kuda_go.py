import os
import time
import requests

from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

URL = os.getenv("url_kuda_go")
API_VERSION = os.getenv("api_version")
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
URL_FOR_REQUEST = f"{URL}/{API_VERSION}"


def to_unixtime() -> int:
    """Получить текущее время в unixtime формате.
    Returns:
        int: 1763715782 unixtime формат, целое число 
    """
    return int(time.mktime(datetime.now().timetuple()))


def to_datetime(unixtime: int) -> str:
    """Преобразовать unixtime в datetime.
    Returns:
        str: возвращается строка вормате "2025-11-21 12:12:25" 
    """
    return str(datetime.fromtimestamp(unixtime))


def get_events() -> dict:
    """Получить список мероприятий
    Returns:
        dict: Возвращается словарь 
        в котором есть ключ results, это список
        словарей с событиями
        {
    "count": 82677,
    "next": "https://kudago.com/public-api/v1.2/events/?fields=age_restriction%2Cis_free&page=2",
    "previous": null,
    "results": [
        {
            "age_restriction": "18+",
            "is_free": false
        },
        ...
    ]
}
    """
    param = {
            "page": 1,
            "page_size": 5,
            "fields": "images,dates,title,place,description,price,publication_date",
            "location": "spb",
            "actual_since": to_unixtime(),
            "text_format":"text"
            }
    url = f"{URL_FOR_REQUEST}/events"
    response = requests.get(url, params=param)
    return response.json()


def get_places(place_id: int|None) -> dict:
    """Получить назвние и адрес места по id.
    Args:
        place_id (int): id места
    Returns:
        dict: Возвращает словарь с адресом, именем места
        {'count': 1,
        'next': None,
        'previous': None,
        'results': [{'address': 'просп. Медиков, д. 3',
              'id': 336,
              'title': 'клуб А2'}]}
    """
    if place_id is None:
        return {}
    param = {
            "page": 1,
            "page_size": 1,
            "fields":"id,title,address",
            "text_format": "text",
            "ids": place_id
            }
    url = f"{URL_FOR_REQUEST}/places"
    response = requests.get(url, params=param)
    return response.json()


def get_collections() -> dict:
    """Получить список подборок редакции
    При тестировании от текущей даты, апи
    возвращает только две актуальных подборки.
    Returns:
        dict: Возвращает словарь с результатами по событиям
       {'count': 1657,
        'next': 'https://kudago.com/public-api/v1.4/lists/?location=spb&page=2&page_size=2',
        'previous': None,
        'results': [{'id': 12525,
              'publication_date': 1767211200,
              'site_url': 'https://kudago.com/all/list/samyie-ozhidaemyie-teatralnyie/',
              'slug': 'samyie-ozhidaemyie-teatralnyie',
              'title': 'Самые ожидаемые театральные фестивали 2025 года'},
             {'id': 7785,
              'publication_date': 1764468010,
              'site_url': 'https://kudago.com/spb/list/glavnye-vystavki-spb/',
              'slug': 'glavnye-vystavki-spb',
              'title': 'Главные выставки ноября в Петербурге'}]} 
    """
    param = {
            "page": 1,
            "page_size": 2,
            "location": "spb",
            "fields": "title,site_url,publication_date",
            "text_format": "text"
            }
    url = f"{URL_FOR_REQUEST}/lists"
    response = requests.get(url, params=param)
    return response.json()


def get_movie_list() -> dict:
    """Получить список фильмов.
    Функция возвращает список словарей в колличестве
    трёх штук, где есть описание фильма, его название,
    дата публикации и ссылка на постер.
    Returns:
        dict: Пример возвращаемого словаря
        {'count': 73,
        'next': 'https://kudago.com/public-api/v1.4/movies/?actual_since=1763969666&fields=id%2Cpublication_date%2Ctitle%2Cdescription%2Cimages&location=spb&page=2&page_size=5',
        'previous': None,
        'results': [{'description': '<p>Романтический отпуск на Лазурном '
                             'побережье.</p>',
              'id': 970,
              'images': [{'image': 'https://media.kudago.com/images/movie/c9/fb/c9fb260c4c9f79c76cc57358e803df6a.jpg',
                          'source': {'link': 'https://www.kinopoisk.ru/film/79427/',
                                     'name': 'kinopoisk.ru'}},
                         {'image': 'https://media.kudago.com/images/movie/89/ce/89ce17268ac96e832b64535feb051b78.jpg',
                          'source': {'link': 'https://www.kinopoisk.ru/film/79427/',
                                     'name': 'kinopoisk.ru'}},
                         {'image': 'https://media.kudago.com/images/movie/69/f8/69f8d76643233383dacd7dce5f49b7d2.webp',
                          'source': {'link': 'https://www.kinopoisk.ru/film/79427/stills/page/1/',
                                     'name': 'kinopoisk.ru'}},
                         {'image': 'https://media.kudago.com/images/movie/2c/f3/2cf3fed4d221a61662e3861a5d678e29.webp',
                          'source': {'link': 'https://www.kinopoisk.ru/film/79427/stills/page/1/',
                                     'name': 'kinopoisk.ru'}}],
              'publication_date': 1417705334,
              'title': 'Бассейн'}, ...
    """
    param = {
        "page": 1,
        "page_size": 3,
        "fields": "id,publication_date,title,description,images",
        "location": "spb",
        "text_format": "text",
        "actual_since": to_unixtime(),
    }
    url = f"{URL_FOR_REQUEST}/movies"
    response = requests.get(url, params=param)
    return response.json()


def get_news() -> dict:
    """Получить новости на сегодняшний день
    Returns:
        dict: Пример вывода
        {'count': 1231,
        'next': 'https://kudago.com/public-api/v1.4/news/?actual_only=True&fields=publication_date%2Ctitle%2Cdescription%2Cimages%2Csite_url&location=spb&page=2&page_size=1',
        'previous': None,
        'results': [{'description': '<p>Каждый календарный день — это целый '
                             'калейдоскоп праздников, за которыми стоят самые '
                             'разнообразные истории, традиции и смыслы. 24 '
                             'ноября на первый взгляд кажется ничем не '
                             'примечательной датой, но стоит заглянуть глубже '
                             '— и перед нами откроется удивительный мир, '
                             'наполненный как древними языческими обрядами, '
                             'так и современными социальными движениями. От '
                             'Домового, пьющего молоко, до торжеств в честь '
                             'японской кухни — всё это празднуется именно в '
                             'этот день</p>',
              'images': [{'image': 'https://media.kudago.com/images/news/e2/08/e2087378c9b65efd72483499222d970c.jpg',
                          'source': {'link': 'https://www.shutterstock.com/ru/image-photo/closeup-walrus-odobenus-rosmarus-colony-on-2359243961',
                                     'name': 'LouieLea/FOTODOM/Shutterstock'}}],
              'publication_date': 1763932208,
              'site_url': 'https://kudago.com/all/news/24-noyabrya-kakoj-prazdnik/',
              'title': '24 ноября: какой праздник сегодня'}]}
    """
    param = {
        "page": 1,
        "page_size": 1,
        "fields": "publication_date,title,description,images,site_url",
        "actual_only": True,
        "location": "spb",
        "text_format": "text"
        }
    url = f"{URL_FOR_REQUEST}/news"
    response = requests.get(url, params=param)
    return response.json()

def date_event(dates: list):
    """Преобразовать список дат в строку
    Обходит список дат, преобразует из unixtime в datetime и сохраняет в строку
    Args:
        dates (list): список словарей с датами
        [
        {'end': 1622448000, 'start': 1618732800},
        {'end': 1633593600, 'start': 1633593600},
        {'end': 1633692600, 'start': 1633692600},
        ...
        ]
    Returns:
        str: С 2025-12-13 00:00:00 по 2026-01-12 00:00:00
    """
    result = ""
    for i in dates:
        start = to_datetime(i.get("start"))
        end = to_datetime(i.get("end"))
        if i.get("start") < to_unixtime():
            continue
        result += f"С {start} по {end}\n"
    return result

def collect_data_for_sending() -> list[dict]:
    """Подготовить данные для отправки
    Функция собирает список с данными по новостям, кино, мероприятиям
    Returns:
        list[dict]: список словарей
    """
    list_of_mesages = []
    # список мероприятий
    events = get_events().get("results")
    for event in events:
        try:
            place_id = event.get("place").get("id")
            place = get_places(place_id).get("results")[0]
        except (TypeError, AttributeError, IndexError):
            place = {}
        
        list_of_mesages.append(
                {
                    "title": event.get("title"),
                    "description": event.get("description"),
                    "publication_date": to_datetime(event.get("publication_date")),
                    "place": place,
                    "price": event.get("price"),
                    "image": event.get("images")[0].get("image"),
                    "dates": date_event(event.get("dates"))
                    }
                )
    # спсиок мероприятий
    collections = get_collections().get("results")
    for collect in collections:
        list_of_mesages.append(
                {
                    "title": collect.get("title"),
                    "publication_date": to_datetime(collect.get("publication_date")),
                    "site_url": collect.get("site_url")
                    }
                )

    # список фильмов
    movies = get_movie_list().get("results")
    for movie in movies:
        list_of_mesages.append(
                {
                    "title": movie.get("title"),
                    "description": movie.get("description"),
                    "publication_date": to_datetime(movie.get("publication_date")),
                    "image": movie.get("images")[0].get("image"),
                    }
                )
    # список новостей
    news = get_news().get("results")
    for tidings in news:
        list_of_mesages.append(
                {
                    "title": tidings.get("title"),
                    "description": tidings.get("description"),
                    "publication_date": to_datetime(tidings.get("publication_date")),
                    "image": tidings.get("images")[0].get("image"),
                    "site_url": tidings.get("site_url")
                    }
                )
    return list_of_mesages


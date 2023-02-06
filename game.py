import random
import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image


def get_spn(coords1, coords2):
    x1, y1 = [float(j) for j in coords1.split()]
    x2, y2 = [float(j) for j in coords2.split()]
    return str(abs(x1 - x2) / 15), str(abs(y1 - y2) / 15)


# Пусть наше приложение предполагает запуск:
# python z4.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)
# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
coords1 = toponym['boundedBy']['Envelope']['lowerCorner']
coords2 = toponym['boundedBy']['Envelope']['upperCorner']
spn = get_spn(coords1, coords2)
print(spn)
new_spn = [str(random.uniform(0.0005, float(min(spn[0], '0.01')))),
           str(random.uniform(0.0005, float(min(spn[1], '0.01'))))]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
# Собираем параметры для запроса к StaticMapsAPI:
toponym_longitude = str(random.uniform(float(toponym_longitude) - float(spn[0]) / 2,
                                       float(toponym_longitude) + float(spn[0]) / 2))
toponym_lattitude = str(random.uniform(float(toponym_lattitude) - float(spn[0]) / 2,
                                       float(toponym_lattitude) + float(spn[0]) / 2))

map_params = {
    "ll": ','.join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join(new_spn),
    "l": random.choice(["map", "sat"]), 'pt': ",".join([toponym_longitude, toponym_lattitude])
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы


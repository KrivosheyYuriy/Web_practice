import math
import requests


# Определяем функцию, считающую расстояние между двумя точками, заданными координатами
def lonlat_distance(a, b):

    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
pt1 = input('Введите название 1й точки: ')
pt2 = input('Введите название 2й точки: ')
response = f"http://geocode-maps.yandex.ru/1.x/?apikey={apikey}&geocode={pt1}&format=json"
response = requests.get(response)
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates1 = [float(j) for j in toponym["Point"]["pos"].split()]
response = f"http://geocode-maps.yandex.ru/1.x/?apikey={apikey}&geocode={pt2}&format=json"
response = requests.get(response)
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates2 = [float(j) for j in toponym["Point"]["pos"].split()]
print(f'Расстояние между точками равно: {lonlat_distance(toponym_coodrinates1, toponym_coodrinates2)} метров')

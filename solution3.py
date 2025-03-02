import sys
import requests
from io import BytesIO
from PIL import Image
from map_utils import calculate_bbox, haversine


GEOCODER_API = "http://geocode-maps.yandex.ru/1.x/"
PLACES_API = "https://search-maps.yandex.ru/v1/"
API_KEY = "https://static-maps.yandex.ru/1.x/"

API_KEYS = {
    'geocoder': '8013b162-6b42-4997-9691-77b7074026e0',
    'places': 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
}


def get_pharmacies(ll):
    params = {
        'apikey': API_KEYS['places'],
        'text': 'аптека',
        'lang': 'ru_RU',
        'll': ll,
        'type': 'biz',
        'results': 10
    }
    response = requests.get(PLACES_API, params=params)
    return response.json().get('features', [])


def get_color(pharmacy):
    hours = pharmacy.get('properties', {}).get(
        'CompanyMetaData', {}).get('Hours', {})
    if not hours:
        return 'gr'

    hours_text = hours.get('text', '').lower()
    if 'круглосуточно' in hours_text:
        return 'gn'

    return 'bl'


def main():
    geocoder_params = {
        'apikey': API_KEYS['geocoder'],
        'geocode': ' '.join(sys.argv[1:]),
        'format': 'json'
    }
    response = requests.get(GEOCODER_API, params=geocoder_params)
    toponym = response.json(
    )['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    src_coords = list(map(float, toponym['Point']['pos'].split()))

    pharmacies = get_pharmacies(f"{src_coords[0]},{src_coords[1]}")

    points = [
        (src_coords[0], src_coords[1], 'pm2rdm')
    ]

    snippets = []
    for pharm in pharmacies:
        coords = pharm['geometry']['coordinates']
        color = get_color(pharm)

        points.append((coords[0], coords[1], f'pm2{color}m'))

        props = pharm['properties']['CompanyMetaData']
        snippets.append({
            'name': props.get('name', 'Нет названия'),
            'address': props.get('address', 'Нет адреса'),
            'hours': props.get('Hours', {}).get('text', 'Нет данных'),
            'distance': haversine(src_coords[0], src_coords[1], coords[0], coords[1])
        })

    center, spn = calculate_bbox([(p[0], p[1]) for p in points])

    map_params = {
        'l': 'map',
        'll': center,
        'spn': spn,
        'pt': '~'.join([f"{p[0]},{p[1]},{p[2]}" for p in points]),
        'size': '650,450'
    }

    response = requests.get(API_KEY, params=map_params)
    Image.open(BytesIO(response.content)).show()

    print("\nРезультаты поиска:")
    for i, snippet in enumerate(snippets, 1):
        print(f"\nАптека #{i}:")
        print(f"Название: {snippet['name']}")
        print(f"Адрес: {snippet['address']}")
        print(f"Время работы: {snippet['hours']}")
        print(f"Расстояние: {snippet['distance']:.0f} м")


if __name__ == "__main__":
    main()

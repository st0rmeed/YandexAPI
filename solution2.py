import sys
import requests
from io import BytesIO
from PIL import Image
from map_utils import calculate_bbox, haversine

geocoder_api = "http://geocode-maps.yandex.ru/1.x/"
places_api = "https://search-maps.yandex.ru/v1/"
static_api = "https://static-maps.yandex.ru/1.x/"

geocoder_key = "8013b162-6b42-4997-9691-77b7074026e0"
places_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address = " ".join(sys.argv[1:])
geocoder_params = {
    "apikey": geocoder_key,
    "geocode": address,
    "format": "json"
}

response = requests.get(geocoder_api, params=geocoder_params)
if not response.ok:
    pass

json_data = response.json()

toponym = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
src_coords = list(map(float, toponym["Point"]["pos"].split()))


places_params = {
    "apikey": places_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": f"{src_coords[0]},{src_coords[1]}",
    "type": "biz",
    "results": 1
}

response = requests.get(places_api, params=places_params)
if not response.ok:
    pass

pharmacy_data = response.json()


pharmacy = pharmacy_data["features"][0]
pharmacy_coords = pharmacy["geometry"]["coordinates"]
pharmacy_props = pharmacy["properties"]["CompanyMetaData"]


distance = haversine(src_coords[0], src_coords[1], *pharmacy_coords)

points = [
    (src_coords[0], src_coords[1], "pm2rdl"),
    (pharmacy_coords[0], pharmacy_coords[1], "pm2gnl")
]

center, spn = calculate_bbox([(p[0], p[1]) for p in points])

map_params = {
    "l": "map",
    "ll": center,
    "spn": spn,
    "pt": "~".join([f"{p[0]},{p[1]},{p[2]}" for p in points])
}

response = requests.get(static_api, params=map_params)


Image.open(BytesIO(response.content)).show()


snippet = f"""
Название: {pharmacy_props.get('name', 'Не указано')}
Адрес: {pharmacy_props.get('address', 'Не указан')}
Время работы: {pharmacy_props.get('Hours', {}).get('text', 'Не указано')}
Расстояние: {distance:.0f} метров
"""

print("Найденная аптека:")
print(snippet.strip())

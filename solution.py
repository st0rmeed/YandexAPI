import sys
from io import BytesIO
import requests
from PIL import Image
from map_scale import get_spn

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": toponym_to_find,
    "format": "json"
}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass

json_response = response.json()


toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


toponym_coords = toponym["Point"]["pos"]
toponym_longitude, toponym_latitude = toponym_coords.split()

spn_lon, spn_lat = get_spn(toponym)

map_api_server = "https://static-maps.yandex.ru/v1"
apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

map_params = {
    "ll": f"{toponym_longitude},{toponym_latitude}",
    "spn": f"{spn_lon:.5f},{spn_lat:.5f}",
    "l": "map",
    "pt": f"{toponym_longitude},{toponym_latitude},pm2rdl",
    "apikey": apikey
}

response = requests.get(map_api_server, params=map_params)

if not response:
    pass

Image.open(BytesIO(response.content)).show()

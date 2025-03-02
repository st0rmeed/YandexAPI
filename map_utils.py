import math


def calculate_bbox(points):
    lons = [float(p[0]) for p in points]
    lats = [float(p[1]) for p in points]

    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)

    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2

    delta_lon = abs(max_lon - min_lon)
    delta_lat = abs(max_lat - min_lat)

    return f"{center_lon},{center_lat}", f"{delta_lon},{delta_lat}"


def haversine(lon1, lat1, lon2, lat2):
    R = 6371
    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a)) * 1000

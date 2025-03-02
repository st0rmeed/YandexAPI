def get_spn(toponym):
    envelope = toponym['boundedBy']['Envelope']
    lower_corner = envelope['lowerCorner'].split()
    upper_corner = envelope['upperCorner'].split()

    lower_lon, lower_lat = map(float, lower_corner)
    upper_lon, upper_lat = map(float, upper_corner)

    delta_lon = upper_lon - lower_lon
    delta_lat = upper_lat - lower_lat

    return delta_lon / 2.0, delta_lat / 2.0

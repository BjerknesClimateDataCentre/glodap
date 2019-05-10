from math import sin, cos, sqrt, atan2, radians

def haversine_distance(lon1, lat1, lon2, lat2):
    """
    Get the approximate distance between two points on the earth, calculated
    using the haversine formula.

    Returns the distance in meters
    """
    # Approx. earth radius, km
    R = 6373.0
    lon1 = radians(lon1)
    lat1 = radians(lat1)
    lon2 = radians(lon2)
    lat2 = radians(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c * 1000

    return distance

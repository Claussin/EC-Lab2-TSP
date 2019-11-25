from collections import deque

class Euc_2D:
    def __init__(self, x = None, y = None):
        self.x = x;
        self.y = y

    def __sub__(self, other):
        return Euc_2D(self.x - other.x, self.y - other.y)

    def norm(self):
        return sqrt(self.x ** 2 + self.y ** 2)

class GeoCoord:
    def __init__(self, degrees = None, minutes = None):
        if degrees < 0:
            (self.degrees, self.minutes) = (degrees, -1 * minutes)
        else:
            (self.degrees, self.minutes) = (degrees, minutes)

    def toRadians(self):
        return (self.degrees + self.minutes / 60) * pi / 180.0

class GeoCity:
    def __init__(self, lat = None, lon = None):
        self.lat = lat.toRadians()
        self.lon = lon.toRadians()

    def coord_tuple(self):
        return (self.lat, self.lon)


def minimal_tsp():
    return {"COMMENT": ""
        , "DIMENSION": None
        , "TYPE": None
        , "EDGE_WEIGHT_TYPE": None
        , "CITIES": []}


def scan_keywords(tsp, tspfile):
    for line in tspfile:
        words = deque(line.split())
        keyword = words.popleft().strip(": ")

        if keyword == "COMMENT":
            tsp["COMMENT"] += " ".join(words).strip(": ")
        elif keyword == "NAME":
            tsp["NAME"] = " ".join(words).strip(": ")
        elif keyword == "TYPE":
            tsp["TYPE"] = " ".join(words).strip(": ")
        elif keyword == "DIMENSION":
            tsp["DIMENSION"] = int(" ".join(words).strip(": "))
        elif keyword == "EDGE_WEIGHT_TYPE":
            tsp["EDGE_WEIGHT_TYPE"] = " ".join(words).strip(": ")
        elif keyword == "NODE_COORD_SECTION":
            break


def read_int(words):
    return int(words.popleft())


def read_euc_2d_city(words):
    x = float(words.popleft())
    y = float(words.popleft())
    return Euc_2D(x, y)


def read_geo_coord(words):
    [degrees, minutes] = map(int, words.popleft().split("."))
    return GeoCoord(degrees, minutes)


def read_geo_city(words):
    lat = read_geo_coord(words)
    lon = read_geo_coord(words)
    return GeoCity(lat, lon)


def read_numbered_geo_city_line(desired_number, words):
    city_number = read_int(words)
    if city_number == desired_number:
        return read_geo_city(words)
    else:
        print("Missing or mislabeld city: expected {0}".format(desired_number))


def read_numbered_euc_2d_city_line(desired_number, words):
    city_number = read_int(words)
    if city_number == desired_number:
        return read_euc_2d_city(words)
    else:
        print("Missing or mislabeld city: expected {0}".format(desired_number))


def read_cities(tsp, tspfile):
    for n in range(1, tsp["DIMENSION"] + 1):
        line = tspfile.readline()
        words = deque(line.split())
        if tsp["EDGE_WEIGHT_TYPE"] == "EUC_2D":
            tsp["CITIES"].append(read_numbered_euc_2d_city_line(n, words))
        elif tsp["EDGE_WEIGHT_TYPE"] == "GEO":
            tsp["CITIES"].append(read_numbered_geo_city_line(n, words))
        else:
            print("Unsupported coordinate type: " + tsp["EDGE_WEIGHT_TYPE"])


def read_tsp_file(path):
    tspfile = open(path, 'r')
    tsp = minimal_tsp()
    scan_keywords(tsp, tspfile)
    read_cities(tsp, tspfile)
    tspfile.close()
    return tsp

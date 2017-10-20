import math
import csv

RADIUS_OF_EARTH = 6378.1
DISTANCE = .03


def directional_point(gps_point, bearing):

    lat1 = math.radians(gps_point[0])
    lon1 = math.radians(gps_point[1])

    lat2 = math.asin(math.sin(lat1) * math.cos(DISTANCE / RADIUS_OF_EARTH) +
                         math.cos(lat1) * math.sin(DISTANCE / RADIUS_OF_EARTH) * math.cos(bearing))

    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(DISTANCE / RADIUS_OF_EARTH) * math.cos(lat1),
                                 math.cos(DISTANCE / RADIUS_OF_EARTH) - math.sin(lat1) * math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    return lat2, lon2


def bearing_between_two_points(gps1, gps2):
    """
    https://gist.github.com/jeromer/2005586

    """
    lat1 = math.radians(gps1[0])
    lat2 = math.radians(gps2[0])

    diffLong = math.radians(gps2[1] - gps1[1])

    x = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))
    y = math.sin(diffLong) * math.cos(lat2)

    initial_bearing = math.degrees(math.atan2(x, y))
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def distance_between_two_points(gps1, gps2):
    lat1 = math.radians(gps1[0])
    lat2 = math.radians(gps2[0])
    dlon = math.radians(gps2[1] - gps1[1])
    dlat = math.radians(gps2[0] - gps1[0])
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = c * RADIUS_OF_EARTH

    return distance * 1000


def main():
    """
    http://www.movable-type.co.uk/scripts/latlong.html
    skip getting all GPS points in first.  Get bearing and next gps point, then calc distance to end point again, rinse
    repeat.
    """

    gps_point_start = (47.372560, -121.811126)
    gps_point_end = (47.408756, -121.741541)

    distance = distance_between_two_points(gps_point_start, gps_point_end)
    bearing = bearing_between_two_points(gps_point_start, gps_point_end)

    number_of_points = int(distance / 30)

    gps_points = []
    gps_points.append(directional_point(gps_point_start, bearing))
    bearing = bearing_between_two_points(gps_points[0], gps_point_end)
    for x in range(number_of_points):
        next_point = directional_point(gps_points[x], bearing)
        gps_points.append(next_point)
        # bearing = bearing_between_two_points(next_point, gps_point_end)
        x += 1

    thecsv = csv.writer(open("map.csv", "w", newline=''))
    for point in gps_points:
        thecsv.writerow(point)

if __name__ == "__main__":
    main()

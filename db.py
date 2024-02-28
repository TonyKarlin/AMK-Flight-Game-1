import os
import geopy.distance
import mysql.connector
import random
from dotenv import load_dotenv

db = {}


def connect_to_db():
    # Loads .env to current os.environ
    load_dotenv()

    # Load database credentials from .env
    # This is to prevent having to commit sensitive information
    # like password and username
    db_variables = {
        'host': os.getenv('HOST'),
        'user': os.getenv('USER'),
        'password': os.getenv('PASSWORD'),
        'database': os.getenv('DATABASE')
    }

    # Connect to SQL-database using the .env variables
    db["database"] = mysql.connector.connect(**db_variables)
    db["cursor"] = db["database"].cursor(dictionary=True)


def get_some_airports():
    db["cursor"].execute(
        f"SELECT * FROM airport ORDER BY RAND() LIMIT 16")
    return db["cursor"].fetchall()


# This function returns 16 random airports, 2 in each direction
# The origin point is the latitude and longitude of the current airport
def draw_airports_from_origin(lat, lon):
    # North, North-East, East, South-East, South, South-West, West, North-West
    flight_bearings = (0, 45, 90, 135, 180, 225, 270, 315)
    flight_points = []
    ports = []
    # Minimum and maximum distance from current airport in miles
    min_dist = 250
    max_dist = 850
    for bearing in flight_bearings:
        distance = random.randint(min_dist, max_dist)
        # Get latitude and longitude of randomly selected place using the origin point
        destination = geopy.distance.distance(miles=distance).destination((lat, lon), bearing=bearing)
        flight_points.append(destination)
    # Find two airports per flight point
    for point in flight_points:
        lat, lon = point[0], point[1]
        db["cursor"].execute(
            f"SELECT * FROM airport ORDER BY ABS({lat} - latitude_deg) + ABS({lon} - longitude_deg) LIMIT 2;")
        airport_data = db["cursor"].fetchmany(2)
        if airport_data:
            for airport in airport_data:
                ports.append(airport)

    return ports


def distance_between_airports(port_1, port_2):
    db["cursor"].execute(
        f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = '{port_1}' OR ident = '{port_2}'")
    airport_data = db["cursor"].fetchmany(2)
    distance = geopy.distance.distance(airport_data[0], airport_data[1])
    return distance


connect_to_db()
# print(distance_between_airports("EFHK", "EFIV"))
# print(get_some_airports())
# print(draw_airports_from_origin(34, 130))

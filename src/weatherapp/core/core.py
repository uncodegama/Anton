import json
import time
import requests

from src.database import perform_db_operation
from src.static import OPEN_WEATHER_MAP_API_KEY
from src.static import LOCATIONS
from src.static import DATABASE_INSERT_INTO_TABLE_WEATHER
from src.static import DATABASE_INSERT_INTO_TABLE_LOCATION
from src.static import DATABASE_SELECT_ALL_TABLE_LOCATION


def call_open_weather_api_predictions():
    try:
        for loc, lat, lon in perform_db_operation(DATABASE_SELECT_ALL_TABLE_LOCATION):
            response = requests.get(
                f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={OPEN_WEATHER_MAP_API_KEY}&units=metric&exclude=minutely")
            perform_db_operation(DATABASE_INSERT_INTO_TABLE_WEATHER,
                                 (loc,
                                  json.dumps(to_location_data(response.json())),
                                  json.dumps(response.json()['current']),
                                  json.dumps(response.json()['hourly']),
                                  json.dumps(response.json()['daily']),
                                  json.dumps(
                                      response.json()['alerts']) if 'alerts' in response.json().keys() else json.dumps({
                                      'alerts': 'null'}),
                                  int(time.time())))

    except Exception as E:
        print("call_open_weather_api_predictions(): " + str(E))


def call_nominatim_api():
    try:
        for loc in LOCATIONS:
            response = requests.get(
                f"https://nominatim.openstreetmap.org/search?city={loc.get('loc_name')}&country={loc.get('country')}&format=json&limit=1")
            perform_db_operation(DATABASE_INSERT_INTO_TABLE_LOCATION,
                                 (loc.get('loc_name'), response.json()[0]['lat'], response.json()[0]['lon']))

    except Exception as E:
        print("call_nominatim_api(): " + str(E))


def to_location_data(data):
    return {
        "lat": data['lat'],
        "lon": data['lon'],
        "timezone": data['timezone'],
        'timezone_offset': data['timezone_offset']
    }

# https://openweathermap.org/current#name
# http://api.openweathermap.org/data/2.5/weather?q=Brno&appid=

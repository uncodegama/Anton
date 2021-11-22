import json
import time
import requests

import anton.utils.database as ad
from anton.utils.constants import OPEN_WEATHER_MAP_API_KEY
from anton.utils.static import LOCATIONS
from anton.utils.static import DATABASE_INSERT_INTO_TABLE_WEATHER
from anton.utils.static import DATABASE_INSERT_INTO_TABLE_LOCATION
from anton.utils.static import DATABASE_SELECT_ALL_TABLE_LOCATION

from anton.utils.logger import logger


def call_open_weather_api_forecasts() -> None:
    try:
        for loc, lat, lon in ad.perform_db_operation(DATABASE_SELECT_ALL_TABLE_LOCATION):
            response = requests.get(
                f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={OPEN_WEATHER_MAP_API_KEY}&units=metric&exclude=minutely")
            ad.perform_db_operation(DATABASE_INSERT_INTO_TABLE_WEATHER,
                                    (loc,
                                     json.dumps(to_location_data(response.json())),
                                     json.dumps(response.json()['current']),
                                     json.dumps(response.json()['hourly']),
                                     json.dumps(response.json()['daily']),
                                     json.dumps(
                                         response.json()[
                                             'alerts']) if 'alerts' in response.json().keys() else json.dumps({
                                         'alerts': 'null'}),
                                     int(time.time())))

    except Exception as e:
        logger.exception(e)


def call_nominatim_api() -> None:
    try:
        for loc in LOCATIONS:
            response = requests.get(
                f"https://nominatim.openstreetmap.org/search?city={loc.get('loc_name')}&country={loc.get('country')}&format=json&limit=1")
            ad.perform_db_operation(DATABASE_INSERT_INTO_TABLE_LOCATION,
                                    (loc.get('loc_name'), response.json()[0]['lat'], response.json()[0]['lon']))

    except Exception as e:
        logger.exception(e)


def to_location_data(data) -> dict:
    return {
        "lat": data['lat'],
        "lon": data['lon'],
        "timezone": data['timezone'],
        'timezone_offset': data['timezone_offset']
    }

# https://openweathermap.org/current#name
# http://api.openweathermap.org/data/2.5/weather?q=Brno&appid=
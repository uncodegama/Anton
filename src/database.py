import sqlite3
import os
from datetime import datetime
import traceback

from src.static import DATABASE_FILE_NAME, DATABASE_CREATE_TABLE_LOCATION, DATABASE_CREATE_TABLE_WEATHER, \
    DATABASE_SELECT_ALL_TABLES, DATABASE_SELECT_TIMESTAMPS_TABLE_WEATHER, UPDATE_TIME
import src.weatherapp.core as wac


def create_db_file() -> None:
    try:
        if find_db_file() is None:
            perform_db_operation(DATABASE_CREATE_TABLE_WEATHER)
            perform_db_operation(DATABASE_CREATE_TABLE_LOCATION)
            wac.call_nominatim_api()
            wac.call_open_weather_api_forecasts()

        elif find_db_file() is not None and perform_db_operation(DATABASE_SELECT_ALL_TABLES)[0][0] == 0:
            perform_db_operation(DATABASE_CREATE_TABLE_WEATHER)
            perform_db_operation(DATABASE_CREATE_TABLE_LOCATION)
            wac.call_nominatim_api()
            wac.call_open_weather_api_forecasts()

        else:
            check_timestamps_and_update_table()

    except Exception as e:
        print("EXCEPTION: create_db_file(): " + str(e))
        print(traceback.print_exc())


def find_db_file(name: str = DATABASE_FILE_NAME):
    for root, dirs, files in os.walk(os.getcwd()):
        if name in files:
            return os.path.join(root, name)
        else:
            return None


def perform_db_operation(db_script: str, data=()) -> list:
    try:
        conn = get_db_connection()
        ret_data = conn.cursor().execute(db_script, data).fetchall()
        conn.commit()
        conn.close()

        if ret_data is not None:
            return ret_data
        else:
            return {}

    except Exception as e:
        print("EXCEPTION: perform_db_operation(): " + str(e))
        print(traceback.print_exc())

    finally:
        conn.close()


def get_db_connection():
    try:
        return sqlite3.connect(os.path.join(os.getcwd(), DATABASE_FILE_NAME))
    except Exception as e:
        print("EXCEPTION: get_db_connection(): " + str(e))
        print(traceback.print_exc())


def check_timestamps_and_update_table() -> None:
    items = perform_db_operation(DATABASE_SELECT_TIMESTAMPS_TABLE_WEATHER)
    timestamps_average = int(sum([a[0] for a in items]) / len(items))

    if timestamps_average + UPDATE_TIME < int(datetime.timestamp(datetime.now())):
        wac.call_open_weather_api_forecasts()

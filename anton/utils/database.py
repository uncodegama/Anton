import os
import sqlite3
from datetime import datetime

from pydantic.typing import Any

import anton.weatherapp.core.core as wac
from anton.utils.logger import logger
from anton.utils.static import (DATABASE_CREATE_TABLE_LOCATION,
                                DATABASE_CREATE_TABLE_WEATHER,
                                DATABASE_FILE_NAME, DATABASE_SELECT_ALL_TABLES,
                                DATABASE_SELECT_TIMESTAMPS_TABLE_WEATHER,
                                UPDATE_TIME)


def create_db_file() -> None:
    try:
        if (
            find_db_file() is None
            or perform_db_operation(DATABASE_SELECT_ALL_TABLES)[0][0] == 0
        ):
            logger.info("Anton.db file was not found OR there weren't any tables.")
            logger.info("Initializing tables - start.")
            perform_db_operation(DATABASE_CREATE_TABLE_WEATHER)
            perform_db_operation(DATABASE_CREATE_TABLE_LOCATION)
            logger.info("Initializing tables - done.")
            logger.info("Calling API - start.")
            wac.call_nominatim_api()
            wac.call_open_weather_api_forecasts()
            logger.info("Calling API - done.")
        else:
            logger.info("Updating data in tables.")
            check_timestamps_and_update_table()

    except Exception as e:
        logger.exception(e)


def find_db_file(name: str = DATABASE_FILE_NAME) -> Any:
    logger.debug(f"Starting to finding file in: {os.getcwd()}")
    for root, dirs, files in os.walk(os.getcwd()):
        if name in files:
            logger.debug("File was found.")
            return os.path.join(root, name)
        else:
            logger.warning("File NOT found.")
            return None


def perform_db_operation(db_script: str, data: tuple = ()) -> list:
    logger.debug(
        f"Opened DB Connection to: {os.path.join(os.getcwd(), DATABASE_FILE_NAME)}"
    )
    with sqlite3.connect(os.path.join(os.getcwd(), DATABASE_FILE_NAME)) as conn:
        logger.info(f"Executing db operation - {db_script}.")
        ret_data = conn.cursor().execute(db_script, data).fetchall()
        conn.commit()

    if ret_data:
        logger.info("Data found in database.")
        return ret_data
    else:
        logger.warning("Data NOT found in database.")
        return []


def check_timestamps_and_update_table() -> None:
    items = perform_db_operation(DATABASE_SELECT_TIMESTAMPS_TABLE_WEATHER)
    timestamps_average = int(sum([a[0] for a in items]) / len(items))
    logger.info(f"Average timestamp is: {timestamps_average}.")

    if timestamps_average + UPDATE_TIME < int(datetime.timestamp(datetime.now())):
        logger.info("Data in database were upgraded.")
        wac.call_open_weather_api_forecasts()

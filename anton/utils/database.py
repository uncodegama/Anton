import os
import sqlite3
from datetime import datetime

from pydantic.typing import Any

import anton.weatherapp.core.core as wac
from anton.utils.logger import logger
from anton.utils.static import (
    DATABASE_CREATE_TABLE_LOCATION,
    DATABASE_CREATE_TABLE_WEATHER,
    DATABASE_DUMP_FILE_NAME,
    DATABASE_FILE_NAME,
    DATABASE_SELECT_TIMESTAMPS_TABLE_WEATHER,
    UPDATE_TIME,
    RunTypeEnum,
)


def create_db_file(run_type: RunTypeEnum = RunTypeEnum.TEST) -> None:
    logger.debug(f"Runtime is: {run_type.name}.")

    if run_type == RunTypeEnum.TEST:
        try:

            # No DB file and No Dump file
            if find_file() is None and find_file(DATABASE_DUMP_FILE_NAME) is None:
                logger.info(
                    f"{DATABASE_FILE_NAME} file was not found OR there weren't any tables."
                )
                logger.info("Initializing tables.")
                perform_db_operation(DATABASE_CREATE_TABLE_WEATHER)
                perform_db_operation(DATABASE_CREATE_TABLE_LOCATION)
                logger.info("Calling API.")
                wac.call_nominatim_api()
                wac.call_open_weather_api_forecasts()

                dump_database_to_sql_file()

            # Dump file Exists
            if find_file(DATABASE_DUMP_FILE_NAME) is not None:
                logger.info(
                    f"Restoring {DATABASE_FILE_NAME} from {DATABASE_DUMP_FILE_NAME}."
                )
                load_database_from_sql_file()

        except Exception as e:
            logger.exception(e)

    if run_type == RunTypeEnum.BUILD:
        try:
            if find_file() is None:
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


def find_file(name: str = DATABASE_FILE_NAME) -> Any:
    logger.debug(f"Starting to finding file - {name} in: {os.getcwd()}")
    for root, dirs, files in os.walk(os.getcwd()):
        if name in files:
            logger.debug(f"File - {name} was found.")
            return os.path.join(root, name)
        else:
            logger.warning(f"File - {name} NOT found.")
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
    logger.info(
        f"Average timestamp is: {timestamps_average} and timestamp now "
        f"is {int(datetime.timestamp(datetime.now()))} "
        f"and delta: {int(datetime.timestamp(datetime.now())) - timestamps_average}."
    )

    if timestamps_average + UPDATE_TIME < int(datetime.timestamp(datetime.now())):
        logger.info("Data in database were upgraded.")
        wac.call_open_weather_api_forecasts()


def dump_database_to_sql_file(
        db_name: str = DATABASE_FILE_NAME, dump_name: str = DATABASE_DUMP_FILE_NAME
) -> None:
    with sqlite3.connect(os.path.join(os.getcwd(), db_name)) as conn:
        with open(os.path.join(os.getcwd(), dump_name), "w") as file:
            logger.debug(
                f"Creating dump file on path {os.path.join(os.getcwd(), dump_name)}."
            )
            for line in conn.iterdump():
                file.write(f"{line}\n")


def load_database_from_sql_file(
        db_name: str = DATABASE_FILE_NAME, dump_name: str = DATABASE_DUMP_FILE_NAME
) -> None:
    with open(os.path.join(os.getcwd(), dump_name), "r") as file:
        with sqlite3.connect(os.path.join(os.getcwd(), db_name)) as conn:
            logger.debug(
                f"Loading dump file on path {os.path.join(os.getcwd(), dump_name)}."
            )
            for line in file.readlines():
                conn.execute(line)

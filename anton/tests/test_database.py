import os
from datetime import datetime

import pytest

import anton.utils.database as aud
from anton.utils.static import (
    DATABASE_FILE_NAME,
    DATABASE_SELECT_ALL_TABLE_LOCATION,
    DATABASE_SELECT_ALL_TABLE_WEATHER,
    DATABASE_SELECT_ALL_TABLES,
    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER,
    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_CURRENT,
    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_DAILY,
    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_HOURLY,
    DATABASE_SELECT_TIMESTAMPS_TABLE_WEATHER,
    UPDATE_TIME,
)


@pytest.mark.order(1)
class TestDatabaseMethods:
    path = os.path.join(os.getcwd(), DATABASE_FILE_NAME)

    # Use actual timestamp - set update time - 1(just to be sure)
    TIMESTAMP = int(datetime.timestamp(datetime.now())) - UPDATE_TIME - 1
    DATABASE_UPDATE_OLD_TIMESTAMP = (
        f"UPDATE weather_forecasts SET timestamp={TIMESTAMP}"
    )

    @pytest.fixture()
    def remove_db_file(self):
        if os.path.exists(self.path):
            os.remove(self.path)
        yield
        if os.path.exists(self.path):
            os.remove(self.path)

    @pytest.mark.usefixtures("remove_db_file")
    def test_create_db_file_none_exist(self):
        assert aud.find_db_file(DATABASE_FILE_NAME) != self.path

        aud.create_db_file()
        assert aud.find_db_file(DATABASE_FILE_NAME) == self.path
        assert aud.perform_db_operation(DATABASE_SELECT_ALL_TABLES)[0][0] == 3

    @pytest.mark.usefixtures("remove_db_file")
    def test_create_db_file_empty_db(self):
        assert aud.find_db_file(DATABASE_FILE_NAME) != self.path

        # touch to create db file, but without data
        aud.perform_db_operation(DATABASE_SELECT_ALL_TABLES)
        assert aud.find_db_file(DATABASE_FILE_NAME) == self.path
        assert aud.perform_db_operation(DATABASE_SELECT_ALL_TABLES)[0][0] == 0

        # fill data to existing db file
        aud.create_db_file()
        assert aud.find_db_file(DATABASE_FILE_NAME) == self.path
        assert aud.perform_db_operation(DATABASE_SELECT_ALL_TABLES)[0][0] == 3

    @pytest.mark.usefixtures("remove_db_file")
    def test_create_db_file_timestamp_update(self):
        assert aud.find_db_file(DATABASE_FILE_NAME) != self.path

        aud.create_db_file()
        assert aud.find_db_file(DATABASE_FILE_NAME) == self.path
        assert aud.perform_db_operation(DATABASE_SELECT_ALL_TABLES)[0][0] == 3

        aud.perform_db_operation(self.DATABASE_UPDATE_OLD_TIMESTAMP)
        items = aud.perform_db_operation(DATABASE_SELECT_TIMESTAMPS_TABLE_WEATHER)
        timestamps_average = int(sum([a[0] for a in items]) / len(items))

        assert timestamps_average == self.TIMESTAMP
        aud.create_db_file()
        items = aud.perform_db_operation(DATABASE_SELECT_TIMESTAMPS_TABLE_WEATHER)
        timestamps_average = int(sum([a[0] for a in items]) / len(items))
        assert timestamps_average != self.TIMESTAMP

    @pytest.mark.usefixtures("remove_db_file")
    def test_find_db_file(self):
        aud.create_db_file()
        assert aud.find_db_file(DATABASE_FILE_NAME) == self.path

    @pytest.mark.usefixtures("remove_db_file")
    def test_data_in_db(self):
        aud.create_db_file()

        # tables
        assert aud.perform_db_operation(DATABASE_SELECT_ALL_TABLES)[0][0] == 3

        # location table
        assert len(aud.perform_db_operation(DATABASE_SELECT_ALL_TABLE_LOCATION)) == 4

        # weather_predictions table
        assert len(aud.perform_db_operation(DATABASE_SELECT_ALL_TABLE_WEATHER)) == 4
        assert (
            len(
                aud.perform_db_operation(
                    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER, (1,)
                )[0]
            )
            == 7
        )
        assert (
            len(
                aud.perform_db_operation(
                    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_CURRENT, (1,)
                )[0]
            )
            == 5
        )
        assert (
            len(
                aud.perform_db_operation(
                    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_HOURLY, (1,)
                )[0]
            )
            == 5
        )
        assert (
            len(
                aud.perform_db_operation(
                    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_DAILY, (1,)
                )[0]
            )
            == 5
        )

########## FILE NAMES ##########

DATABASE_FILE_NAME = "Anton.db"
LOGGER_FILE_NAME = "Anton.log"

########## STATIC VARIABLES ##########

LOCATIONS = [
    {"loc_name": "Brno", "country": "Czechia"},
    {"loc_name": "Nové Mesto nad Váhom", "country": "Slovakia"},
    {"loc_name": "Skalica", "country": "Slovakia"},
    {"loc_name": "Spišská Nová Ves", "country": "Slovakia"},
]

# seconds
UPDATE_TIME = 1800

########## DEFAULT QUERIES ##########

DATABASE_SELECT_ALL_TABLES = """
SELECT count(name) FROM sqlite_master WHERE type='table'
"""

########## WEATHER FORECASTS ##########

DATABASE_CREATE_TABLE_WEATHER = """
CREATE TABLE IF NOT EXISTS weather_forecasts ([id] INTEGER PRIMARY KEY, [location] TEXT,[data] TEXT, [current] TEXT, [hourly] TEXT, [daily] TEXT, [alerts] TEXT, [timestamp] TIMESTAMP)
"""

DATABASE_INSERT_INTO_TABLE_WEATHER = """
INSERT OR REPLACE INTO weather_forecasts (id, location, data, current, hourly, daily, alerts, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

DATABASE_SELECT_TIMESTAMPS_TABLE_WEATHER = """
SELECT timestamp FROM weather_forecasts
"""

########## WEATHER SINGLE ##########


DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER = """
SELECT id, location, data, current, hourly, daily, alerts FROM weather_forecasts WHERE id = (?)
"""

DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_CURRENT = """
SELECT id, location, data, current, alerts FROM weather_forecasts WHERE id = (?)
"""

DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_HOURLY = """
SELECT id, location, data, hourly, alerts FROM weather_forecasts WHERE id = (?)
"""

DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_DAILY = """
SELECT id, location, data, daily, alerts FROM weather_forecasts WHERE id = (?)
"""

########## WEATHER ALL ##########

DATABASE_SELECT_TABLE_WEATHER_CURRENTS = """
SELECT id, location, data, current, alerts FROM weather_forecasts
"""

########## LOCATION ##########

DATABASE_CREATE_TABLE_LOCATION = """
CREATE TABLE IF NOT EXISTS location ([id] INTEGER PRIMARY KEY AUTOINCREMENT,[location] TEXT, [lat] TEXT, [lon] TEXT)
"""

DATABASE_INSERT_INTO_TABLE_LOCATION = """
INSERT OR REPLACE INTO location (location, lat, lon) VALUES (?, ?, ?)
"""

DATABASE_SELECT_ALL_TABLE_LOCATION = """
SELECT * FROM location
"""

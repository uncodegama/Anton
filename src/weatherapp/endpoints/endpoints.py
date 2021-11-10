from fastapi import APIRouter

from src.weatherapp.models.locationModel import Location, LocationModel
from src.weatherapp.models.weatherPredictionDailyModel import WeatherPredictionDailyModel, WeatherPredictionDaily
from src.weatherapp.models.weatherPredictionModel import WeatherPrediction, WeatherPredictionModel
from src.weatherapp.models.weatherPredictionCurrentModel import WeatherPredictionCurrentModel, WeatherPredictionCurrent
from src.weatherapp.models.weatherPredictionHourlyModel import WeatherPredictionHourlyModel, WeatherPredictionHourly

from src.database import perform_db_operation
from src.static import DATABASE_SELECT_ALL_TABLE_LOCATION, DATABASE_SELECT_ALL_TABLE_WEATHER, \
    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER, DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_CURRENT, \
    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_HOURLY, DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_DAILY

weather = APIRouter(
    prefix="/weather",
    tags=["weather"],
    responses={404: {"description": "Not found"}}
)


@weather.get("/locations",
             response_model=list[LocationModel],
             description="Returns all locations and their latitude and longitude from database.")
async def get_locations():
    return [Location(*location).__dict__ for location in perform_db_operation(DATABASE_SELECT_ALL_TABLE_LOCATION)]


@weather.get("/predictions",
             response_model=list[WeatherPredictionModel],
             description="Returns all weather predictions for all locations in database. - Not recommended to use!")
async def get_weather_predictions():
    return [WeatherPrediction(*weather) for weather in perform_db_operation(DATABASE_SELECT_ALL_TABLE_WEATHER)]


@weather.get("/predictions/{location}",
             response_model=WeatherPredictionModel,
             description="Returns weather prediction (current, hourly, daily) for given location.")
async def get_weather_prediction_by_location(location: str):
    return WeatherPrediction(*perform_db_operation(DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER, (location,))[0])


@weather.get("/predictions/{location}/current",
             response_model=WeatherPredictionCurrentModel,
             description="Returns current weather prediction for given location. {1}")
async def get_weather_prediction_by_location_current(location: str):
    return WeatherPredictionCurrent(
        *perform_db_operation(DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_CURRENT, (location,))[0])


@weather.get("/predictions/{location}/hourly",
             response_model=WeatherPredictionHourlyModel,
             description="Returns hourly weather prediction for given location, for 48 hours. [{48}]")
async def get_weather_prediction_by_location_hourly(location: str):
    return WeatherPredictionHourly(
        *perform_db_operation(DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_HOURLY, (location,))[0])


@weather.get("/predictions/{location}/daily",
             response_model=WeatherPredictionDailyModel,
             description="Returns daily weather prediction for given location, for 7 days (today included). [{8}]")
async def get_weather_prediction_by_location_daily(location: str):
    return WeatherPredictionDaily(
        *perform_db_operation(DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_DAILY, (location,))[0])

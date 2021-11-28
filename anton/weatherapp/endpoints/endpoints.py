from fastapi import APIRouter, HTTPException

from anton.utils.database import perform_db_operation
from anton.utils.static import (
    DATABASE_SELECT_ALL_TABLE_LOCATION, DATABASE_SELECT_ALL_TABLE_WEATHER,
    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER,
    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_CURRENT,
    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_DAILY,
    DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_HOURLY)
from anton.weatherapp.models.location_model import Location, LocationModel
from anton.weatherapp.models.weather_forecast_current_model import (
    WeatherForecastCurrent, WeatherForecastCurrentModel)
from anton.weatherapp.models.weather_forecast_daily_model import (
    WeatherForecastDaily, WeatherForecastDailyModel)
from anton.weatherapp.models.weather_forecast_hourly_model import (
    WeatherForecastHourly, WeatherForecastHourlyModel)
from anton.weatherapp.models.weather_forecast_model import (
    WeatherForecast, WeatherForecastModel)

weather = APIRouter(
    prefix="/weather",
    tags=["weather"],
    responses={404: {"description": "Not found."}},
)


@weather.get(
    "/locations",
    response_model=list[LocationModel],
    description="Returns all locations and their latitude and longitude from database.",
)
async def get_locations():
    query = perform_db_operation(DATABASE_SELECT_ALL_TABLE_LOCATION)
    if not query:
        raise HTTPException(status_code=404, detail="Locations not found.")
    return [Location(*location) for location in query]


@weather.get(
    "/forecasts",
    response_model=list[WeatherForecastModel],
    description="Returns all weather forecasts for all locations in database. - Not recommended to use!",
)
async def get_weather_forecasts():
    query = perform_db_operation(DATABASE_SELECT_ALL_TABLE_WEATHER)
    if not query:
        raise HTTPException(status_code=404, detail="Forecasts not found.")
    return [WeatherForecast(*weather) for weather in query]


@weather.get(
    "/forecasts/{location}",
    response_model=WeatherForecastModel,
    description="Returns weather forecast (current, hourly, daily) for given location.",
)
async def get_weather_forecast_by_location(location: str) -> WeatherForecast:
    query = perform_db_operation(DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER, (location,))
    if not query:
        raise HTTPException(status_code=404, detail="Forecast not found.")
    return WeatherForecast(*query[0])


@weather.get(
    "/forecasts/{location}/current",
    response_model=WeatherForecastCurrentModel,
    description="Returns current weather forecast for given location. {1}",
)
async def get_weather_forecast_by_location_current(
    location: str,
) -> WeatherForecastCurrent:
    query = perform_db_operation(
        DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_CURRENT, (location,)
    )
    if not query:
        raise HTTPException(status_code=404, detail="Forecast not found.")
    return WeatherForecastCurrent(*query[0])


@weather.get(
    "/forecasts/{location}/hourly",
    response_model=WeatherForecastHourlyModel,
    description="Returns hourly weather forecast for given location, for 48 hours. [{48}]",
)
async def get_weather_forecast_by_location_hourly(
    location: str,
) -> WeatherForecastHourly:
    query = perform_db_operation(
        DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_HOURLY, (location,)
    )
    if not query:
        raise HTTPException(status_code=404, detail="Forecast not found.")
    return WeatherForecastHourly(*query[0])


@weather.get(
    "/forecasts/{location}/daily",
    response_model=WeatherForecastDailyModel,
    description="Returns daily weather forecast for given location, for 7 days (today included). [{8}]",
)
async def get_weather_forecast_by_location_daily(location: str) -> WeatherForecastDaily:
    query = perform_db_operation(
        DATABASE_SELECT_BY_LOCATION_TABLE_WEATHER_DAILY, (location,)
    )
    if not query:
        raise HTTPException(status_code=404, detail="Forecast not found.")
    return WeatherForecastDaily(*query[0])

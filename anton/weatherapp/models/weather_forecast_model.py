import json

from pydantic import BaseModel
from pydantic.typing import List, Optional, Union


class WeatherForecast(object):
    def __init__(
        self,
        location: str,
        data: Union[str, bytes],
        current: Union[str, bytes],
        hourly: Union[str, bytes],
        daily: Union[str, bytes],
        alerts: Union[str, bytes],
    ) -> None:
        self.location: str = location
        self.data = json.loads(data)
        self.current = json.loads(current)
        self.hourly = json.loads(hourly)
        self.daily = json.loads(daily)
        self.alerts = json.loads(alerts)


class WeatherForecastModel(BaseModel):
    location: str = "Brno"
    data: dict = {
        "lat": 49.1922,
        "lon": 16.6113,
        "timezone": "Europe/Prague",
        "timezone_offset": 7200,
    }
    current: dict = {}
    hourly: list[dict] = [{}]
    daily: list[dict] = [{}]
    alerts: Optional[List[dict]] = [{}]

    class Config:
        orm_mode = True

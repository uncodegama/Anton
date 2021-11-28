import json

from pydantic import BaseModel
from pydantic.typing import List, Optional


class WeatherForecastDaily(object):
    def __init__(self, location, data, daily, alerts):
        self.location: str = location
        self.data = json.loads(data)
        self.daily = json.loads(daily)
        self.alerts = json.loads(alerts)


class WeatherForecastDailyModel(BaseModel):
    location: str = "Brno"
    data: dict = {
        "lat": 49.1922,
        "lon": 16.6113,
        "timezone": "Europe/Prague",
        "timezone_offset": 7200,
    }
    daily: list[dict] = [{}]
    alerts: Optional[List[dict]] = [{}]

    class Config:
        orm_mode = True

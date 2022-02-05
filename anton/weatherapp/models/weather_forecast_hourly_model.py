import json

from pydantic import BaseModel
from pydantic.typing import List, Optional


class WeatherForecastHourly(object):
    def __init__(self, id, location, data, hourly, alerts):
        self.id: int = id
        self.location: str = location
        self.data = json.loads(data)
        self.hourly = json.loads(hourly)
        self.alerts = json.loads(alerts)


class WeatherForecastHourlyModel(BaseModel):
    id: int = 1
    location: str = "Brno"
    data: dict = {
        "lat": 49.1922,
        "lon": 16.6113,
        "timezone": "Europe/Prague",
        "timezone_offset": 7200,
    }
    hourly: list[dict] = [{}]
    alerts: Optional[List[dict]] = [{}]

    class Config:
        orm_mode = True

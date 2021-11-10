import json

from pydantic import BaseModel
from pydantic.typing import Optional


class WeatherPrediction(object):
    def __init__(self, location, data, current, hourly, daily, alerts):
        self.location: str = location
        self.data = json.loads(data)
        self.current = json.loads(current)
        self.hourly = json.loads(hourly)
        self.daily = json.loads(daily)
        self.alerts = json.loads(alerts)


class WeatherPredictionModel(BaseModel):
    location: str = "Brno"
    data: dict = {"lat": 49.1922, "lon": 16.6113, "timezone": "Europe/Prague", "timezone_offset": 7200}
    current: dict = {}
    hourly: list[dict] = {}
    daily: list[dict] = {}
    alerts: Optional[dict] = {}

    class Config:
        orm_mode = True

import json

from pydantic import BaseModel
from pydantic.typing import Optional


class WeatherPredictionCurrent(object):
    def __init__(self, location, data, current, alerts):
        self.location: str = location
        self.data = json.loads(data)
        self.current = json.loads(current)
        self.alerts = json.loads(alerts)


class WeatherPredictionCurrentModel(BaseModel):
    location: str = "Brno"
    data: dict = {"lat": 49.1922, "lon": 16.6113, "timezone": "Europe/Prague", "timezone_offset": 7200}
    current: dict = {}
    alerts: Optional[dict] = {}

    class Config:
        orm_mode = True

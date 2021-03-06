import json

from pydantic import BaseModel
from pydantic.typing import List, Optional


class WeatherForecastCurrent(object):
    def __init__(self, id, location, data, current, alerts):
        self.id: int = id
        self.location: str = location
        self.data = json.loads(data)
        self.current = json.loads(current)
        self.alerts = json.loads(alerts)


class WeatherForecastCurrentModel(BaseModel):
    id: int = 1
    location: str = "Brno"
    data: dict = {
        "lat": 49.1922,
        "lon": 16.6113,
        "timezone": "Europe/Prague",
        "timezone_offset": 7200,
    }
    current: dict = {}
    alerts: Optional[List[dict]] = [{}]

    class Config:
        orm_mode = True

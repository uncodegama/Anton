from pydantic import BaseModel


class Location(object):
    def __init__(self, location, lat, lon):
        self.location: str = location
        self.lat: str = lat
        self.lon: str = lon


class LocationModel(BaseModel):
    location: str = "Brno"
    lat: str = "49.1922443"
    lon: str = "16.6113382"

    class Config:
        orm_mode = True

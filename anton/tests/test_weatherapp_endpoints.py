from fastapi.testclient import TestClient

from anton.main import app
from anton.utils.database import create_db_file


class TestWeatherAppEndpoints:
    client = TestClient(app())

    @classmethod
    def setup_class(cls):
        create_db_file()

    def test_get_locations(self):
        response = self.client.get("weather/locations")
        assert response.status_code == 200
        assert len(response.json()) == 4
        assert response.json()[0]['location'] == 'Brno'
        assert response.json()[0]['location'] != 'brno'
        assert response.json()[0]['lat'] == '49.1922443'
        assert response.json()[0]['lon'] == '16.6113382'

    def test_get_weather_forecasts(self):
        response = self.client.get("weather/forecasts")
        assert response.status_code == 200
        assert len(response.json()) == 4

    def test_get_weather_forecast_by_location(self):
        response = self.client.get("weather/forecasts/Brno")
        assert response.status_code == 200
        assert len(response.json()) == 6
        assert response.json()['location'] == 'Brno'
        assert response.json()['data']['lat'] == '49.1922'
        assert response.json()['data']['lon'] == '16.6113'

    def test_get_weather_forecast_by_location_current(self):
        response = self.client.get("weather/forecasts/Brno/current")
        assert response.status_code == 200

    def test_get_weather_forecast_by_location_hourly(self):
        response = self.client.get("weather/forecasts/Brno/hourly")
        assert response.status_code == 200

    def test_get_weather_forecast_by_location_daily(self):
        response = self.client.get("weather/forecasts/Brno/daily")
        assert response.status_code == 200



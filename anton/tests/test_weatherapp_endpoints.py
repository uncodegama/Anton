from fastapi.testclient import TestClient

from anton.main import app

client = TestClient(app())


def test_get_locations_status():
    response = client.get("weather/locations")
    assert response.status_code == 200


def test_get_locations_data():
    response = client.get("weather/locations")
    assert len(response.json()) == 4
    assert response.json()[0]['location'] == 'Brno'
    assert response.json()[0]['location'] != 'brno'
    assert response.json()[0]['lat'] == '49.1922443'
    assert response.json()[0]['lon'] == '16.6113382'


def test_get_weather_forecast_by_location_status():
    response = client.get("weather/forecasts/Brno")
    assert response.status_code == 200


def test_get_weather_forecast_by_location_data():
    response = client.get("weather/forecasts/Brno")
    assert len(response.json()) == 6
    assert response.json()['location'] == 'Brno'
    assert response.json()['data']['lat'] == '49.1922'

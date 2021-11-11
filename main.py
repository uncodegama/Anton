from fastapi import FastAPI

from src.weatherapp.endpoints.endpoints import weather
from src.database import create_db_file
from src.common import timer_run
from src.static import UPDATE_TIME

import src.weatherapp.core.core as c

app = FastAPI(
    title="Anton v2.0",
    description="Backend for Anton application.")

app.include_router(weather)

create_db_file()
timer_run(UPDATE_TIME, c.call_open_weather_api_forecasts)

# python -m uvicorn main:app --reload

# python -m pip freeze > requirements.txt
# python -m pip install -r requirements.txt

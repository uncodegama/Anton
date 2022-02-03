import os
import threading
import time

import psutil
import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

import anton.weatherapp.core.core as core
from anton.utils.common import timer_run
from anton.utils.database import create_db_file
from anton.utils.static import UPDATE_TIME
from anton.weatherapp.endpoints.endpoints import weather


def app():
    app = FastAPI(title="Anton v2.0", description="Backend for Anton application.")
    app.include_router(weather)

    def self_terminate():
        time.sleep(1)
        parent = psutil.Process(os.getpid())
        parent.kill()

    @app.post(
        "/kill", description="Kills the uvicorn server.", status_code=status.HTTP_200_OK
    )
    async def kill():
        threading.Thread(target=self_terminate, daemon=True).start()
        return {"success": True}

    origins = (["http://localhost:8080"],)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


if __name__ == "__main__":
    create_db_file()
    timer_run(UPDATE_TIME, core.call_open_weather_api_forecasts)

    uvicorn.run(app(), host="127.0.0.1", port=8000, log_level="info")

# python -m uvicorn main:app --reload

# python -m pip freeze > requirements.txt
# python -m pip install -r requirements.txt
# python -m pip install -e .
# isort .

# Anton

<p align="center">
  <a href="https://github.com/uncodegama/Anton"><img src="https://github.com/uncodegama/Anton/blob/master/static/Anton_logo.JPG?raw=true" alt="Anton"></a>
</p>

[![Test](https://github.com/uncodegama/Anton/actions/workflows/test.yml/badge.svg)](https://github.com/uncodegama/Anton/actions/workflows/test.yml) [![Current Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/uncodegama/Anton) [![Python Version](https://img.shields.io/badge/python-3.9-green)](https://www.python.org/downloads/release/python-396/) 

---
"Everybody has Siri and Alexa, I'm going to have Anton!" - uncodegama

Anton is meant to be an unintuitive and unintelligent home assistant, that is being created as a free-time project. The plan is to create RPI based touchscreen application, that will show actual time, current weather and weather predictions and play online radio or podcasts (maybe much more in the future).

---
## Technology Stack
The plan is to use (if it's possible):
 * <a href="https://www.python.org/">Python</a> as Backend -> Project Link: <a href="https://github.com/uncodegama/Anton"> Backend Part </a>
 * <a href="https://vuejs.org/">Vue.js</a> as Frontend -> Project Link: N/A
 * <a href="https://www.electronjs.org/">Electron</a> to pack it all up -> Project Link: N/A
 
---
## Requirements

* Python 3.9
* <a href="https://github.com/uncodegama/Anton/blob/master/pyproject.toml"> Used Packages </a>
* <a href="https://openweathermap.org/">OpenWeatherMap</a> API key, which will be stored in ```anton/utils/constants.py``` as ```OPEN_WEATHER_MAP_API_KEY = <YOUR_API_KEY>``` (P.S. - You need to create that file)

---
## Installation
```
python -m pip install flit
flit install
python -m uvicorn main:app --reload
```

or:
```
run main.py
```

and go to:
```
localhost:8000/docs
```

### Location change

if you want to add your places to show current weather and weather predictions, go to <a href="https://github.com/uncodegama/Anton/blob/master/anton/utils/static.py">(link)</a>:
```
anton/utils/static.py
```

and change LOCATIONS (Now there are only my important locations - planed to be more intuitive in future):
```
LOCATIONS = {
    {
        "loc_name": "<your_city_name>",
        "country": "<country>"
    },
}
```

Example:
```
LOCATIONS = {
    {
        "loc_name": "Brno",
        "country": "Czechia"
    }
}
```




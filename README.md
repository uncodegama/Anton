# Anton

<p align="center">
  <a href="https://github.com/uncodegama/Anton"><img src="https://github.com/uncodegama/Anton/blob/master/static/Anton_logo.JPG?raw=true" alt="Anton"></a>
</p>

[![Current Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/uncodegama/Anton) [![Python Version](https://img.shields.io/badge/python-3.9-green)](https://www.python.org/downloads/release/python-396/) 

---
"Everybody has Siri and Alexa, I'm going to have Anton!" - uncodegama

Anton is meant to be an unintuitive and unintelligent home assistant, that is being created as a past-time project. The plan is to create RPI based touchscreen application, that will show actual time, current weather and weather predictions and play online radio or podcasts (maybe much more in the future).

---
## Technology Stack
The plan is to use (if it's possible):
 * <a href="https://www.python.org/">Python</a> as Backend -> Project Link: <a href="https://github.com/uncodegama/Anton"> Backend Part </a>
 * <a href="https://vuejs.org/">Vue.js</a> as Frontend -> Project Link: N/A
 * <a href="https://www.electronjs.org/">Electron</a> to pack it all up -> Project Link: N/A
 
---
## Requirements

* Python 3.9
* <a href="https://github.com/uncodegama/Anton/blob/master/requirements.txt"> Used Packages </a>

---
## Installation
```
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```



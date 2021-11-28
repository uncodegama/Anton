cd %~dp0
cd ..

python -m mypy anton
python -m flake8 --ignore E501,E266,W503 anton
python -m black anton
python -m isort .
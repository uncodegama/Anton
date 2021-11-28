#!/usr/bin/env bash

set -e
set -x

mypy anton
flake8 --ignore E501,E266,W503 anton
black anton --check
isort anton --check-only
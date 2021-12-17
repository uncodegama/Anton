#!/usr/bin/env bash

set -e
set -x

pyinstaller --onefile --clean --name Anton --console --key=$1  ./anton/main.py



#!/usr/bin/env bash

set -e
set -x

pyinstaller --onefile --icon=static/64x64.ico --clean --name Anton --console --upx-dir /home/runner/work/Anton/Anton/upx-3.96-arm64_linux --key=$1  ./anton/main.py
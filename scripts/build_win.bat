@echo off

set arg1=%1

pyinstaller --onefile --icon=static/64x64.ico --clean --name Anton --console --upx-dir C:\upx-3.96-win64 --key=%arg1%  ./anton/main.py

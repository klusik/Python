@echo off
REM Create the development environment using only the local wheelhouse directory.
setlocal
cd /d "%~dp0\.."

if not exist wheelhouse (
    echo The wheelhouse directory does not exist.
    echo Run scripts\download_wheels.bat on an internet-connected matching PC first.
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    py -3.12 -m venv .venv 2>nul
    if errorlevel 1 py -3.11 -m venv .venv
    if errorlevel 1 exit /b 1
)

call .venv\Scripts\activate.bat
python -m pip install --no-index --find-links wheelhouse "setuptools>=80" wheel
if errorlevel 1 exit /b 1
python -m pip install --no-index --find-links wheelhouse -r requirements-dev.txt
if errorlevel 1 exit /b 1
python -m pip install --no-index --no-build-isolation --no-deps -e .
if errorlevel 1 exit /b 1

echo.
echo Offline development environment is ready.
endlocal

@echo off
setlocal

cd /d "%~dp0"

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python was not found in PATH.
    echo Install Python 3.11 or newer and try again.
    pause
    exit /b 1
)

echo Installing requirements...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip.
    pause
    exit /b 1
)

python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements.
    pause
    exit /b 1
)

echo Starting ACARS Virtual Printer...
start "" pythonw "%~dp0AVP.pyw"
exit /b 0

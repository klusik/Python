@echo off
setlocal

where py >nul 2>nul
if errorlevel 1 (
    echo Python launcher "py" was not found.
    echo Install Python for Windows and make sure the launcher is available.
    pause
    exit /b 1
)

py -c "import PIL, mutagen, imageio_ffmpeg" >nul 2>nul
if errorlevel 1 (
    echo Installing required libraries...
    py -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Dependency installation failed.
        pause
        exit /b 1
    )
)

start "" pyw main.pyw
exit /b 0

@echo off
REM Download a Windows wheelhouse for later installation without internet access.
setlocal
cd /d "%~dp0\.."

where py >nul 2>nul
if errorlevel 1 (
    echo Python launcher "py" was not found.
    exit /b 1
)

if not exist wheelhouse mkdir wheelhouse
py -3.12 -m pip download --dest wheelhouse -r requirements-dev.txt "setuptools>=80" wheel
if errorlevel 1 (
    py -3.11 -m pip download --dest wheelhouse -r requirements-dev.txt "setuptools>=80" wheel
    if errorlevel 1 exit /b 1
)

echo.
echo Wheelhouse created in %CD%\wheelhouse
endlocal

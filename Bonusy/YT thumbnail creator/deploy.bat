@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem Build a single-file portable EXE with PyInstaller and clean temporary output.
rem Place this file in the root folder of the project, next to app.py.

cd /d "%~dp0"

set "APP_NAME=youtube_thumbnail_creator"
set "ENTRY_FILE=app.py"
set "SPEC_FILE=%APP_NAME%.spec"
set "DIST_DIR=dist"
set "BUILD_DIR=build"
set "OUTPUT_EXE=%APP_NAME%.exe"

echo.
echo ==================================================
echo Building %OUTPUT_EXE%
echo ==================================================
echo.

rem Basic sanity checks.
if not exist "%ENTRY_FILE%" (
    echo ERROR: Entry file "%ENTRY_FILE%" was not found in:
    echo %cd%
    exit /b 1
)

python --version >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python is not available in PATH.
    echo Install Python or add it to PATH first.
    exit /b 1
)

python -m PyInstaller --version >nul 2>nul
if errorlevel 1 (
    echo ERROR: PyInstaller is not installed for this Python interpreter.
    echo Install it with:
    echo     pip install pyinstaller
    exit /b 1
)

rem Remove any previous output file at project root.
if exist "%OUTPUT_EXE%" (
    del /f /q "%OUTPUT_EXE%" >nul 2>nul
)

rem Clean PyInstaller working folders from previous runs.
if exist "%DIST_DIR%" (
    rmdir /s /q "%DIST_DIR%" >nul 2>nul
)
if exist "%BUILD_DIR%" (
    rmdir /s /q "%BUILD_DIR%" >nul 2>nul
)
if exist "%SPEC_FILE%" (
    del /f /q "%SPEC_FILE%" >nul 2>nul
)

rem Build onefile executable.
rem --collect-all PIL helps package Pillow more reliably.
python -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --onefile ^
    --windowed ^
    --name "%APP_NAME%" ^
    --collect-all PIL ^
    "%ENTRY_FILE%"

if errorlevel 1 (
    echo.
    echo ERROR: PyInstaller build failed.
    goto :cleanup
)

rem Move the final EXE from dist\ to the project root.
if not exist "%DIST_DIR%\%OUTPUT_EXE%" (
    echo.
    echo ERROR: Expected output file was not created:
    echo %DIST_DIR%\%OUTPUT_EXE%
    goto :cleanup
)

move /y "%DIST_DIR%\%OUTPUT_EXE%" "%OUTPUT_EXE%" >nul
if errorlevel 1 (
    echo.
    echo ERROR: Failed to move EXE to project root.
    goto :cleanup
)

echo.
echo Build succeeded:
echo %cd%\%OUTPUT_EXE%

:cleanup
rem Always clean temporary build artifacts.
if exist "%DIST_DIR%" (
    rmdir /s /q "%DIST_DIR%" >nul 2>nul
)
if exist "%BUILD_DIR%" (
    rmdir /s /q "%BUILD_DIR%" >nul 2>nul
)
if exist "%SPEC_FILE%" (
    del /f /q "%SPEC_FILE%" >nul 2>nul
)

echo.
echo Temporary build folders cleaned.

if exist "%OUTPUT_EXE%" (
    echo Final EXE is ready in project root.
    exit /b 0
) else (
    echo Final EXE was not created.
    exit /b 1
)

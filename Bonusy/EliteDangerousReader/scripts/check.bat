@echo off
REM Run linting, formatting verification, type checking, and tests.
setlocal
cd /d "%~dp0\.."

if not exist ".venv\Scripts\python.exe" (
    call scripts\setup_venv.bat
    if errorlevel 1 exit /b 1
)

call .venv\Scripts\activate.bat
ruff check src tests run_elite_reader.py
if errorlevel 1 exit /b 1
ruff format --check src tests run_elite_reader.py
if errorlevel 1 exit /b 1
mypy
if errorlevel 1 exit /b 1
pytest
if errorlevel 1 exit /b 1

echo.
echo All checks passed.
endlocal

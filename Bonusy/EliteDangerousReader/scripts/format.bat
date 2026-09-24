@echo off
REM Apply automated Python lint fixes and formatting.
setlocal
cd /d "%~dp0\.."

if not exist ".venv\Scripts\python.exe" (
    call scripts\setup_venv.bat
    if errorlevel 1 exit /b 1
)

call .venv\Scripts\activate.bat
ruff check --fix src tests run_elite_reader.py
if errorlevel 1 exit /b 1
ruff format src tests run_elite_reader.py
endlocal

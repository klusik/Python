@echo off
REM Run Elite Dangerous Reader from the local virtual environment.
setlocal
cd /d "%~dp0\.."

if not exist ".venv\Scripts\python.exe" (
    call scripts\setup_venv.bat
    if errorlevel 1 exit /b 1
)

call .venv\Scripts\activate.bat
python -m elite_reader %*
endlocal

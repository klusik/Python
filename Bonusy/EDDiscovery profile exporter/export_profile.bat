@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 "%~dp0elite_profile_exporter.py" --commander KlusikCZ --output "%~dp0elite_profile.json" --include-event-summary
) else (
    python "%~dp0elite_profile_exporter.py" --commander KlusikCZ --output "%~dp0elite_profile.json" --include-event-summary
)

if errorlevel 1 (
    echo.
    echo Export failed. Review the error above.
    pause
    exit /b 1
)

echo.
echo Export complete: %~dp0elite_profile.json
pause

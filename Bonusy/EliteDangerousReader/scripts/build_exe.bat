@echo off
REM Validate the repository and build the one-file Windows executable.
setlocal
cd /d "%~dp0\.."

if not exist ".venv\Scripts\python.exe" (
    call scripts\setup_venv.bat
    if errorlevel 1 exit /b 1
)

call .venv\Scripts\activate.bat
call scripts\check.bat
if errorlevel 1 exit /b 1

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
pyinstaller --noconfirm --clean EliteDangerousReader.spec
if errorlevel 1 exit /b 1

echo.
echo Built executable:
echo %CD%\dist\EliteDangerousReader.exe
endlocal

@echo off
setlocal

set "APP_NAME=WASM clearer"
set "SCRIPT_DIR=%~dp0"
set "TARGET_SCRIPT=%SCRIPT_DIR%WASM_clear.pyw"
set "START_MENU_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\%APP_NAME%"
set "SHORTCUT_PATH=%START_MENU_DIR%\%APP_NAME%.lnk"

if not exist "%TARGET_SCRIPT%" (
  echo Could not find "%TARGET_SCRIPT%".
  exit /b 1
)

where pyw >nul 2>nul
if errorlevel 1 (
  echo Python launcher "pyw" was not found on PATH.
  echo Install Python for Windows or add the launcher to PATH, then try again.
  exit /b 1
)

if not exist "%START_MENU_DIR%" mkdir "%START_MENU_DIR%"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$wsh = New-Object -ComObject WScript.Shell; " ^
  "$lnk = $wsh.CreateShortcut($env:SHORTCUT_PATH); " ^
  "$lnk.TargetPath = (Get-Command pyw).Source; " ^
  "$lnk.Arguments = ('\"' + $env:TARGET_SCRIPT + '\"'); " ^
  "$lnk.WorkingDirectory = $env:SCRIPT_DIR; " ^
  "$lnk.WindowStyle = 1; " ^
  "$lnk.Description = 'MSFS WASM Cache Cleaner'; " ^
  "$lnk.Save()"

if errorlevel 1 (
  echo Failed to create the Start Menu shortcut.
  exit /b 1
)

echo Created Start Menu shortcut at:
echo %SHORTCUT_PATH%
exit /b 0

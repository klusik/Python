@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

set "APP_NAME=AVP"
set "ENTRY_FILE=AVP.pyw"
set "ICON_FILE=%TEMP%\avp_build_icon.ico"

python --version >nul 2>&1
if errorlevel 1 (
    echo Python was not found in PATH.
    pause
    exit /b 1
)

echo Installing build dependencies...
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

echo Building icon used by PyInstaller...
python -c "from PIL import Image, ImageDraw; image = Image.new('RGBA', (256, 256), (255, 255, 255, 0)); draw = ImageDraw.Draw(image); draw.rounded_rectangle((20, 20, 236, 236), radius=40, fill=(25, 118, 210, 255)); draw.rectangle((64, 52, 192, 78), fill=(255, 255, 255, 255)); draw.rectangle((64, 100, 192, 126), fill=(255, 255, 255, 255)); draw.rectangle((64, 148, 160, 174), fill=(255, 255, 255, 255)); image.save(r'%ICON_FILE%')"
if errorlevel 1 (
    echo Failed to create build icon.
    pause
    exit /b 1
)

echo Removing previous build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "%APP_NAME%.spec" del /q "%APP_NAME%.spec"
if exist "%APP_NAME%.exe" del /q "%APP_NAME%.exe"

echo Creating standalone executable...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "%APP_NAME%" --icon "%ICON_FILE%" "%ENTRY_FILE%"
if errorlevel 1 (
    echo PyInstaller build failed.
    if exist "%ICON_FILE%" del /q "%ICON_FILE%"
    pause
    exit /b 1
)

echo Moving executable to project root...
copy /y "dist\%APP_NAME%.exe" "%APP_NAME%.exe" >nul
if errorlevel 1 (
    echo Failed to copy executable to project root.
    if exist "%ICON_FILE%" del /q "%ICON_FILE%"
    pause
    exit /b 1
)

echo Cleaning generated helper files and folders...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "%APP_NAME%.spec" del /q "%APP_NAME%.spec"
if exist "%ICON_FILE%" del /q "%ICON_FILE%"

echo.
echo Build finished successfully.
echo Output: %CD%\%APP_NAME%.exe
pause
exit /b 0

@echo off
setlocal

set APP_NAME=YouTube Downloader
set EXE_NAME=YouTube Downloader.exe
set FFMPEG_ARGS=

if not exist ".venv" (
    py -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "import tkinter" || (
    echo Tkinter is not available in this Python installation.
    echo Install Python with Tcl/Tk support before packaging.
    exit /b 1
)

for /f "delims=" %%F in ('where ffmpeg 2^>nul') do (
    if not defined FFMPEG_ARGS set FFMPEG_ARGS=--add-binary "%%F;."
)

for /f "delims=" %%F in ('where ffprobe 2^>nul') do (
    set FFMPEG_ARGS=%FFMPEG_ARGS% --add-binary "%%F;."
)

pyinstaller --noconfirm --clean --onefile --windowed --name "%APP_NAME%" %FFMPEG_ARGS% ytd.pyw

if exist "%EXE_NAME%" del "%EXE_NAME%"
copy "dist\%EXE_NAME%" "%EXE_NAME%"

rmdir /s /q build
rmdir /s /q dist
if exist "%APP_NAME%.spec" del "%APP_NAME%.spec"

echo Created "%EXE_NAME%" in the project root.
endlocal

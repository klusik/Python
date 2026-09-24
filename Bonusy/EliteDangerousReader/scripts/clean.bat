@echo off
REM Remove generated build output and development caches.
setlocal
cd /d "%~dp0\.."

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist .mypy_cache rmdir /s /q .mypy_cache
if exist .ruff_cache rmdir /s /q .ruff_cache
if exist .coverage del /q .coverage
for /d /r %%D in (__pycache__) do @if exist "%%D" rmdir /s /q "%%D"
for /d /r %%D in (*.egg-info) do @if exist "%%D" rmdir /s /q "%%D"

echo Build and cache directories removed.
endlocal

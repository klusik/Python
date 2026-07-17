@echo off
setlocal EnableExtensions

rem Always execute relative to the project directory, regardless of the caller's
rem current PowerShell directory.
pushd "%~dp0" >nul 2>&1
if errorlevel 1 (
    echo Deployment failed: unable to enter the project directory.
    exit /b 1
)

set "PYTHON_COMMAND="
where py >nul 2>&1
if not errorlevel 1 set "PYTHON_COMMAND=py -3"

if not defined PYTHON_COMMAND (
    where python >nul 2>&1
    if not errorlevel 1 set "PYTHON_COMMAND=python"
)

if not defined PYTHON_COMMAND (
    echo Deployment failed: Python 3 was not found in PATH.
    popd >nul 2>&1
    exit /b 1
)

%PYTHON_COMMAND% scripts\create_deploy.py
set "DEPLOY_EXIT_CODE=%ERRORLEVEL%"

popd >nul 2>&1

if not "%DEPLOY_EXIT_CODE%"=="0" (
    echo Deployment failed with exit code %DEPLOY_EXIT_CODE%.
    exit /b %DEPLOY_EXIT_CODE%
)

echo Deployment completed successfully.
exit /b 0

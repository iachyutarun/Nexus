@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
set PYTHONPATH=%~dp0;%PYTHONPATH%
python "%~dp0nexus\app\main.py"
if errorlevel 1 (
    echo.
    echo Failed to start NEXUS. Ensure Python is installed and in PATH.
    pause
)

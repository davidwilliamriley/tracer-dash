@echo off
:: Tracer.bat - Dash App Launcher for Tracer-Dash Application
:: This batch file starts the Dash delivery manager application

:: To-Do - Add support for Virtual Environments

echo.
echo ========================================
echo   TRACER-DASH APPLICATION LAUNCHER
echo ========================================
echo.

:: Change to the application directory (where the batch file is located)
cd /d "%~dp0"
echo Current directory: %cd%

:: Look for app.py in current directory first
if exist "app.py" (
    echo Found app.py in current directory
) else (
    :: If not found, try looking in common subdirectories
    if exist "app\app.py" (
        cd app
        echo Navigating to app subdirectory...
        echo New directory: %cd%
    ) else if exist "src\app.py" (
        cd src
        echo Navigating to src subdirectory...
        echo New directory: %cd%
    ) else (
        echo ERROR: app.py not found in current directory or common subdirectories
        echo Current directory: %cd%
        echo.
        echo Available files and directories:
        dir /b
        echo.
        echo Looking for app.py in:
        echo - Current directory: %cd%
        echo - app subdirectory: %cd%\app
        echo - src subdirectory: %cd%\src
        echo.
        pause
        exit /b 1
    )
)

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

:: Check if Dash is installed
python -c "import dash" >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Dash is not installed
    echo Installing Dash and required packages...
    echo.
    python -m pip install dash pandas plotly
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install required packages
        pause
        exit /b 1
    )
)

:: Display startup information
echo Starting Tracer-Dash Application...
echo.
echo Application will be available at: http://localhost:8050
echo Press Ctrl+C in this window to stop the application
echo.

:: Start the Dash application
echo Starting application...
python app.py

:: If we get here, the app has stopped
echo.
echo Application stopped.
pause
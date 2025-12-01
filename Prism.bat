@echo off
:: Tracer.bat - Dash App Launcher for Tracer-Dash Application
:: This batch file starts the Dash delivery manager application with virtual environment support

echo.
echo ========================================
echo   TRACER-DASH APPLICATION LAUNCHER
echo ========================================
echo.

:: Change to the Application Directory (where the batch file is located)
cd /d "%~dp0"
echo Current Directory: %cd%

:: Set the Virtual Environment Directory (at root level)
set "ROOT_DIR=%cd%"
set "VENV_DIR=%ROOT_DIR%\.venv"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "VENV_ACTIVATE=%VENV_DIR%\Scripts\activate.bat"

:: Check if Python is Installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and Re-try the Application
    pause
    exit /b 1
)

:: Check if .venv exists, create if it doesn't (at Root Level)
if not exist "%VENV_DIR%\" (
    echo Virtual Environment not found. Creating new Virtual Environment at .venv...
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create Virtual Environment
        echo Make sure you have venv module available to the Application
        pause
        exit /b 1
    )
    echo Virtual Environment created successfully at .venv
) else (
    echo Virtual Environment found at .venv
)

:: Activate the Virtual Environment
echo Activating the Virtual Environment...
call "%VENV_ACTIVATE%"
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate the Virtual Environment
    pause
    exit /b 1
)

:: Check if Dash is installed in the .venv
"%VENV_PYTHON%" -c "import dash" >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Dash is not installed in the Virtual Environment
    echo Installing Dash and the Required Packages...
    echo.
    "%VENV_PYTHON%" -m pip install dash pandas plotly
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install the required Packages
        pause
        exit /b 1
    )
)

:: Look for app.py in the Current Directory
if exist "app.py" (
    echo Found app.py in Current Directory
) else (
    :: If not found, try looking in common Subdirectories
    if exist "app\app.py" (
        cd app
        echo Navigating to the app Subdirectory...
        echo New Directory: %cd%
    ) else if exist "src\app.py" (
        cd src
        echo Navigating to src Subdirectory...
        echo New Directory: %cd%
    ) else (
        echo ERROR: app.py not found in Current Directory or common Subdirectories
        echo Current Directory: %cd%
        echo.
        echo Available Files and Directories:
        dir /b
        echo.
        echo Looking for app.py in:
        echo - Current Ddirectory: %cd%
        echo - app Subdirectory: %cd%\app
        echo - src Subdirectory: %cd%\src
        echo.
        pause
        exit /b 1
    )
)

:: Display startup Information
echo Starting the Tracer-Dash Application...
echo Using the Virtual Environment @ .venv
echo.
echo Application available at: http://localhost:8050
echo Press Ctrl+C in this Window to stop the Application
echo.

:: Start the Dash application using the .venv Python Interpreter
echo Starting Application...
"%VENV_PYTHON%" app.py

:: If we get here, the app has stopped
echo.
echo Application Stopped.
pause
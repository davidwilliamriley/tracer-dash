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

:: Set virtual environment Directory (at root level)
set "ROOT_DIR=%cd%"
set "VENV_DIR=%ROOT_DIR%\.venv"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "VENV_ACTIVATE=%VENV_DIR%\Scripts\activate.bat"

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

:: Check if .venv exists, create if it doesn't (at Root Level)
if not exist "%VENV_DIR%\" (
    echo Virtual environment not found. Creating new virtual environment at .venv...
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        echo Make sure you have venv module available
        pause
        exit /b 1
    )
    echo Virtual environment created successfully at .venv
) else (
    echo Virtual environment found at .venv
)

:: Activate virtual environment
echo Activating virtual environment...
call "%VENV_ACTIVATE%"
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
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
        echo ERROR: Failed to install required Packages
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
        echo Navigating to app Subdirectory...
        echo New directory: %cd%
    ) else if exist "src\app.py" (
        cd src
        echo Navigating to src Subdirectory...
        echo New directory: %cd%
    ) else (
        echo ERROR: app.py not found in Current Directory or common Subdirectories
        echo Current directory: %cd%
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
echo Starting Tracer-Dash Application...
echo Using virtual environment: .venv
echo.
echo Application will be available at: http://localhost:8050
echo Press Ctrl+C in this window to stop the Application
echo.

:: Start the Dash application using the .venv Python Interpreter
echo Starting Application...
"%VENV_PYTHON%" app.py

:: If we get here, the app has stopped
echo.
echo Application stopped.
pause
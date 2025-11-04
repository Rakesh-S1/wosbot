@echo off
echo =======================================
echo  Wosland Discord Bot - Quick Setup
echo =======================================
echo.

REM Check for --clear argument
set CLEAR_MODE=false
if "%1"=="--clear" set CLEAR_MODE=true
if "%1"=="-c" set CLEAR_MODE=true

REM Check for --no-update argument
set UPDATE_MODE=false
if "%1"=="--no-update" set UPDATE_MODE=false
if "%2"=="--no-update" set UPDATE_MODE=false

REM Check for AUTO_UPDATE in .env (for production)
if exist .env (
    findstr /C:"AUTO_UPDATE=true" .env >nul
    if not errorlevel 1 (
        set UPDATE_MODE=true
    )
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Check if git is available and update code
if "%UPDATE_MODE%"=="true" (
    echo [1/6] Checking for updates from Git...
    git --version >nul 2>&1
    if not errorlevel 1 (
        echo Pulling latest changes from repository...
        git pull origin main
        if errorlevel 1 (
            echo [WARNING] Failed to pull updates, continuing with local version...
        ) else (
            echo Code updated successfully!
        )
    ) else (
        echo Git not found, skipping auto-update...
    )
    echo.
) else (
    echo [INFO] Auto-update skipped
    echo.
)

echo [2/6] Checking virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
) else (
echo [2/6] Checking virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
) else (
    echo Virtual environment found!
)

echo.
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo [4/6] Checking and installing dependencies...
echo Verifying all requirements are installed...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo All dependencies are installed!

echo.
echo [5/6] Checking for .env file...
if not exist .env (
    echo .env file not found. Creating from template...
    copy .env.example .env
    echo.
    echo [ACTION REQUIRED]
    echo Please edit .env file and add your Discord bot token
    echo Then run this script again
    pause
    exit /b 0
)

echo.
echo Checking .env configuration...
findstr /C:"your_bot_token_here" .env >nul
if not errorlevel 1 (
    echo [WARNING] .env file still has placeholder token
    echo Please edit .env and add your real Discord bot token
    pause
    exit /b 0
)

echo.
echo [6/6] Starting bot...
echo.

REM Set CLEAR_COMMANDS in .env if --clear was used
if "%CLEAR_MODE%"=="true" (
    echo [CLEAR MODE] Enabling command clearing...
    powershell -Command "(Get-Content .env) -replace 'CLEAR_COMMANDS=false', 'CLEAR_COMMANDS=true' | Set-Content .env"
    echo This will clear outdated commands and sync new ones.
    echo.
) else (
    REM Check if CLEAR_COMMANDS is already set to true in .env
    findstr /C:"CLEAR_COMMANDS=true" .env >nul
    if not errorlevel 1 (
        echo [CLEAR MODE] Clearing old Discord commands...
        echo This will clear outdated commands and sync new ones.
        echo.
    )
)

echo Bot is running... Press Ctrl+C to stop
echo =======================================
echo.
python bot.py

REM Reset CLEAR_COMMANDS to false if we set it
if "%CLEAR_MODE%"=="true" (
    echo.
    echo Resetting CLEAR_COMMANDS to false...
    powershell -Command "(Get-Content .env) -replace 'CLEAR_COMMANDS=true', 'CLEAR_COMMANDS=false' | Set-Content .env"
)

pause

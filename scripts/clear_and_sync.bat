@echo off
echo =======================================
echo  Clear Discord Commands
echo =======================================
echo.
echo This will clear all old Discord commands
echo and sync new ones from your updated code.
echo.
echo Use this when:
echo  - Commands show as "outdated"
echo  - You added/removed/changed commands
echo  - Discord shows old command versions
echo.
pause

REM Go to parent directory (project root)
cd /d "%~dp0.."

echo.
echo Setting CLEAR_COMMANDS=true...

REM Temporarily set the flag in .env
powershell -Command "(Get-Content .env) -replace 'CLEAR_COMMANDS=false', 'CLEAR_COMMANDS=true' | Set-Content .env"

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting bot with command clearing...
python bot.py

echo.
echo Resetting CLEAR_COMMANDS=false...
powershell -Command "(Get-Content .env) -replace 'CLEAR_COMMANDS=true', 'CLEAR_COMMANDS=false' | Set-Content .env"

echo.
echo Commands cleared! Restarting bot normally...
timeout /t 2 /nobreak >nul

echo.
echo Bot is running... Press Ctrl+C to stop
echo =======================================
echo.
python bot.py

pause

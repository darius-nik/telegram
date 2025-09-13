@echo off
echo 🤖 Starting Admin Group Bot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "admin_group_bot.py" (
    echo ❌ admin_group_bot.py not found
    pause
    exit /b 1
)

if not exist "config.py" (
    echo ❌ config.py not found
    pause
    exit /b 1
)

echo ✅ All required files found
echo 🚀 Starting bot...
echo.

REM Start the bot
python start_admin_bot.py

echo.
echo Bot stopped. Press any key to exit...
pause >nul

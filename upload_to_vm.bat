@echo off
REM اسکریپت آپلود فایل‌های پروژه به ماشین مجازی
REM Upload Project Files to Virtual Machine

echo 🤖 Telegram Bot VM Upload Script
echo ================================

REM دریافت اطلاعات ماشین مجازی
set /p VM_IP="Enter VM IP address: "
set /p VM_USER="Enter VM username: "
set /p VM_PATH="Enter VM path (default: ~/telegram-bot): "

if "%VM_PATH%"=="" set VM_PATH=~/telegram-bot

echo.
echo 📋 Upload Configuration:
echo VM IP: %VM_IP%
echo VM User: %VM_USER%
echo VM Path: %VM_PATH%
echo.

REM بررسی وجود فایل‌های پروژه
if not exist "admin_group_bot.py" (
    echo ❌ admin_group_bot.py not found!
    echo Please run this script from the project directory.
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ❌ requirements.txt not found!
    echo Please run this script from the project directory.
    pause
    exit /b 1
)

echo ✅ Project files found
echo.

REM آپلود فایل‌ها
echo 📤 Uploading project files...

REM آپلود فایل‌های Python
scp admin_group_bot.py %VM_USER%@%VM_IP%:%VM_PATH%/
scp start_admin_bot.py %VM_USER%@%VM_IP%:%VM_PATH%/
scp test_admin_bot.py %VM_USER%@%VM_IP%:%VM_PATH%/
scp config.py %VM_USER%@%VM_IP%:%VM_PATH%/

REM آپلود فایل‌های متنی
scp requirements.txt %VM_USER%@%VM_IP%:%VM_PATH%/
scp *.md %VM_USER%@%VM_IP%:%VM_PATH%/

REM آپلود اسکریپت نصب
scp install.sh %VM_USER%@%VM_IP%:%VM_PATH%/

if %errorlevel% equ 0 (
    echo ✅ Files uploaded successfully!
    echo.
    echo 📋 Next steps:
    echo 1. Connect to VM: ssh %VM_USER%@%VM_IP%
    echo 2. Run installation: bash %VM_PATH%/install.sh
    echo 3. Edit config: nano %VM_PATH%/config.py
    echo 4. Start bot: sudo systemctl start telegram-bot
    echo.
) else (
    echo ❌ Upload failed!
    echo Please check your connection and credentials.
)

echo.
echo Press any key to exit...
pause > nul

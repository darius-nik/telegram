@echo off
echo 🤖 راه‌اندازی ربات تلگرام هوشمند
echo =====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python نصب نیست. لطفاً Python 3.8+ را نصب کنید.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ⚠️  فایل .env یافت نشد. ایجاد فایل نمونه...
    copy .env.example .env
    echo ✅ فایل .env ایجاد شد.
    echo ⚠️  لطفاً توکن‌های خود را در فایل .env قرار دهید.
    pause
    exit /b 1
)

REM Install requirements if needed
if not exist venv (
    echo 🔄 ایجاد محیط مجازی...
    python -m venv venv
)

echo 🔄 فعال‌سازی محیط مجازی...
call venv\Scripts\activate.bat

echo 🔄 نصب وابستگی‌ها...
pip install -r requirements.txt

echo 🧪 اجرای تست‌ها...
python test_bot.py
if errorlevel 1 (
    echo ❌ تست‌ها ناموفق بودند. لطفاً خطاها را بررسی کنید.
    pause
    exit /b 1
)

echo ✅ همه چیز آماده است!
echo 🚀 اجرای ربات...
python run.py

pause



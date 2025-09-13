#!/bin/bash

echo "🤖 راه‌اندازی ربات تلگرام هوشمند"
echo "====================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python نصب نیست. لطفاً Python 3.8+ را نصب کنید."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  فایل .env یافت نشد. ایجاد فایل نمونه..."
    cp .env.example .env
    echo "✅ فایل .env ایجاد شد."
    echo "⚠️  لطفاً توکن‌های خود را در فایل .env قرار دهید."
    exit 1
fi

# Install requirements if needed
if [ ! -d "venv" ]; then
    echo "🔄 ایجاد محیط مجازی..."
    python3 -m venv venv
fi

echo "🔄 فعال‌سازی محیط مجازی..."
source venv/bin/activate

echo "🔄 نصب وابستگی‌ها..."
pip install -r requirements.txt

echo "🧪 اجرای تست‌ها..."
python test_bot.py
if [ $? -ne 0 ]; then
    echo "❌ تست‌ها ناموفق بودند. لطفاً خطاها را بررسی کنید."
    exit 1
fi

echo "✅ همه چیز آماده است!"
echo "🚀 اجرای ربات..."
python run.py

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8079917344:AAF-SJi9EixwuwlSAuQW55BJ9XhAsPJs-Rk')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv()
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///telegram_bot.db')
    
    # Redis Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Application Configuration
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    TIMEZONE = os.getenv('TIMEZONE', 'Asia/Tehran')
    MAX_REMINDERS_PER_USER = int(os.getenv('MAX_REMINDERS_PER_USER', '10'))
    MAX_AI_REQUESTS_PER_DAY = int(os.getenv('MAX_AI_REQUESTS_PER_DAY', '50'))
    
    # External APIs
    COINGECKO_API_URL = os.getenv('COINGECKO_API_URL', 'https://api.coingecko.com/api/v3')
    
    # Bot Messages (Persian)
    WELCOME_MESSAGE = """
🤖 سلام! به ربات هوشمند خوش آمدید!

من می‌توانم به شما کمک کنم:

🧠 سوالات شما را با هوش مصنوعی پاسخ دهم
⏰ یادآوری تنظیم کنم
📷 متن تصاویر را بخوانم (OCR)
💰 قیمت ارزهای دیجیتال را بگویم
🌍 متن‌ها را ترجمه کنم

برای شروع از دستورات زیر استفاده کنید:
/start - شروع
/help - راهنما
/ask - سوال از هوش مصنوعی
/remind - تنظیم یادآوری
/ocr - خواندن متن تصویر
/crypto - قیمت ارز دیجیتال
/translate - ترجمه متن
"""
    
    HELP_MESSAGE = """
📖 راهنمای استفاده از ربات:

🧠 /ask [سوال شما] - سوال از هوش مصنوعی
⏰ /remind [زمان] [متن] - تنظیم یادآوری
📷 /ocr - ارسال تصویر برای خواندن متن
💰 /crypto [نام ارز] - قیمت ارز دیجیتال
🌍 /translate [متن] - ترجمه متن
📊 /stats - آمار استفاده شما
❓ /help - نمایش این راهنما

مثال‌ها:
/ask بهترین روش یادگیری برنامه‌نویسی چیست؟
/remind 2 ساعت بعد خرید نان
/crypto bitcoin
/translate Hello world
"""

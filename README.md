# 🤖 Admin Group Bot - ربات مدیریت گروه ادمین

ربات تلگرام برای مدیریت گروه‌هایی که فقط ادمین‌ها اجازه ارسال پیام دارند.

## ✨ ویژگی‌ها

- 🔒 **مدیریت دسترسی**: فقط ادمین‌ها می‌توانند پیام ارسال کنند
- 🗑️ **حذف خودکار**: پیام‌های کاربران عادی فوراً حذف می‌شوند
- 📝 **ارسال مجدد**: پیام‌های حذف شده با نام کاربر ارسال می‌شوند
- 🛡️ **سیستم ضد اسپم**: جلوگیری از ارسال پیام‌های مکرر
- 📱 **پشتیبانی از رسانه**: عکس، ویدیو، استیکر، فایل و...
- ⚡ **عملکرد بالا**: پردازش سریع پیام‌ها با سیستم صف

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.8 یا بالاتر
- حساب تلگرام و Bot Token
- سرور (اختیاری - می‌توانید روی کامپیوتر شخصی هم اجرا کنید)

### 1️⃣ کلون کردن پروژه

```bash
git clone https://github.com/yourusername/admin-group-bot.git
cd admin-group-bot
```

### 2️⃣ نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### 3️⃣ تنظیم Bot Token

1. به [@BotFather](https://t.me/botfather) در تلگرام پیام دهید
2. دستور `/newbot` را ارسال کنید
3. نام و username ربات را انتخاب کنید
4. Token دریافتی را در فایل `config.py` قرار دهید:

```python
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
```

### 4️⃣ اجرای ربات

#### روی کامپیوتر شخصی:
```bash
python start_admin_bot.py
```

#### روی سرور Linux:
```bash
# اجرای مستقیم
python3 start_admin_bot.py

# یا با systemd (برای اجرای دائمی)
sudo systemctl start admin-group-bot
```

#### روی سرور Windows:
```cmd
start_admin_bot.bat
```

## 🐳 اجرا با Docker

### 1️⃣ ساخت و اجرای کانتینر

```bash
# ساخت image
docker build -t admin-group-bot .

# اجرای کانتینر
docker run -d --name admin-group-bot \
  -e TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN \
  admin-group-bot
```

### 2️⃣ با Docker Compose

```bash
# ویرایش docker-compose.yml و قرار دادن token
docker-compose up -d
```

## 📋 دستورات ربات

| دستور | توضیح |
|-------|--------|
| `/start` | شروع ربات و نمایش راهنما |
| `/help` | نمایش راهنمای کامل |
| `/setup` | تنظیم ربات در گروه |
| `/status` | نمایش وضعیت ربات و لیست ادمین‌ها |
| `/refresh_admins` | بروزرسانی لیست ادمین‌ها |
| `/unmute` | حذف سکوت کاربر (ادمین) |
| `/spam_mode` | فعال/غیرفعال کردن ضد اسپم برای ادمین‌ها |

## 🔧 تنظیمات

### متغیرهای محیطی

```bash
# فایل .env
TELEGRAM_BOT_TOKEN=your_bot_token_here
DEBUG=True
TIMEZONE=Asia/Tehran
```

### تنظیمات پیشرفته

در فایل `config.py` می‌توانید تنظیمات زیر را تغییر دهید:

- `MAX_REMINDERS_PER_USER`: حداکثر تعداد یادآوری برای هر کاربر
- `MAX_AI_REQUESTS_PER_DAY`: حداکثر درخواست AI در روز
- `TIMEZONE`: منطقه زمانی

## 🖥️ راه‌اندازی روی سرور

### سرور VPS (Ubuntu/Debian)

#### 1️⃣ آماده‌سازی سرور

```bash
# بروزرسانی سیستم
sudo apt update && sudo apt upgrade -y

# نصب Python و pip
sudo apt install python3 python3-pip git -y

# کلون کردن پروژه
git clone https://github.com/yourusername/admin-group-bot.git
cd admin-group-bot

# نصب وابستگی‌ها
pip3 install -r requirements.txt
```

#### 2️⃣ تنظیم systemd service

```bash
# ایجاد فایل سرویس
sudo nano /etc/systemd/system/admin-group-bot.service
```

محتوای فایل:

```ini
[Unit]
Description=Admin Group Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/admin-group-bot
ExecStart=/usr/bin/python3 start_admin_bot.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/home/ubuntu/admin-group-bot

[Install]
WantedBy=multi-user.target
```

#### 3️⃣ فعال‌سازی و اجرای سرویس

```bash
# بارگذاری مجدد systemd
sudo systemctl daemon-reload

# فعال‌سازی سرویس
sudo systemctl enable admin-group-bot

# شروع سرویس
sudo systemctl start admin-group-bot

# بررسی وضعیت
sudo systemctl status admin-group-bot

# مشاهده لاگ‌ها
sudo journalctl -u admin-group-bot -f
```

### سرور VPS (CentOS/RHEL)

```bash
# نصب Python
sudo yum install python3 python3-pip git -y

# بقیه مراحل مشابه Ubuntu است
```

### سرور Windows Server

1. Python را از [python.org](https://python.org) دانلود و نصب کنید
2. پروژه را کلون کنید
3. وابستگی‌ها را نصب کنید: `pip install -r requirements.txt`
4. فایل `start_admin_bot.bat` را اجرا کنید

## 🔍 تست و عیب‌یابی

### تست اتصال ربات

```bash
python test_admin_bot.py
```

### بررسی لاگ‌ها

```bash
# مشاهده لاگ‌های زنده
tail -f bot.log

# یا با systemd
sudo journalctl -u admin-group-bot -f
```

### مشکلات رایج

#### ❌ ربات پیام‌ها را حذف نمی‌کند
- بررسی کنید ربات دسترسی ادمین دارد
- دستور `/setup` را دوباره اجرا کنید
- از `/refresh_admins` استفاده کنید

#### ❌ خطای "Bot was blocked by the user"
- کاربر ربات را بلاک کرده است
- این خطا طبیعی است و ربات به کار خود ادامه می‌دهد

#### ❌ خطای اتصال
- اتصال اینترنت را بررسی کنید
- Token ربات را بررسی کنید
- فایروال سرور را بررسی کنید

## 📊 مانیتورینگ

### بررسی وضعیت سرویس

```bash
# وضعیت سرویس
sudo systemctl status admin-group-bot

# استفاده از CPU و RAM
htop

# لاگ‌های سیستم
sudo journalctl -u admin-group-bot --since "1 hour ago"
```

### آمار استفاده

ربات به صورت خودکار آمار استفاده را در لاگ‌ها ثبت می‌کند.

## 🔒 امنیت

### توصیه‌های امنیتی

1. **Token ربات را محرمانه نگه دارید**
2. **از HTTPS استفاده کنید**
3. **فایروال سرور را تنظیم کنید**
4. **به‌روزرسانی‌های امنیتی را نصب کنید**

### تنظیم فایروال

```bash
# Ubuntu/Debian
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## 🤝 مشارکت

برای مشارکت در پروژه:

1. پروژه را Fork کنید
2. شاخه جدید ایجاد کنید: `git checkout -b feature/amazing-feature`
3. تغییرات را commit کنید: `git commit -m 'Add amazing feature'`
4. شاخه را push کنید: `git push origin feature/amazing-feature`
5. Pull Request ایجاد کنید

## 📝 مجوز

این پروژه تحت مجوز MIT منتشر شده است. برای جزئیات بیشتر فایل [LICENSE](LICENSE) را مطالعه کنید.

## 📞 پشتیبانی

- 🐛 **گزارش باگ**: [Issues](https://github.com/yourusername/admin-group-bot/issues)
- 💡 **پیشنهاد ویژگی**: [Discussions](https://github.com/yourusername/admin-group-bot/discussions)
- 📧 **ایمیل**: your-email@example.com

## ⭐ ستاره دادن

اگر این پروژه برای شما مفید بود، لطفاً یک ستاره ⭐ بدهید!

---

**نکته**: این ربات برای مدیریت گروه‌های تلگرام طراحی شده که فقط ادمین‌ها اجازه ارسال پیام دارند. قبل از استفاده، قوانین و مقررات تلگرام را مطالعه کنید.

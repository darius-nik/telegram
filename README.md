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

**روش 1 - تنظیم مستقیم در config.py (ساده‌تر):**

1. فایل `config.py` را باز کنید
2. خط 9 را پیدا کنید: `TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')`
3. `YOUR_BOT_TOKEN_HERE` را با token واقعی جایگزین کنید:

```python
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '123456789:ABCdefGHIjklMNOpqrsTUVwxyz')
```

**روش 2 - استفاده از فایل .env (امن‌تر):**

1. فایل `env.example` را کپی کنید: `cp env.example .env`
2. فایل `.env` را ویرایش کنید و token واقعی را قرار دهید:

```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
DEBUG=True
TIMEZONE=Asia/Tehran
```

**دریافت Bot Token:**
1. به [@BotFather](https://t.me/botfather) در تلگرام پیام دهید
2. دستور `/newbot` را ارسال کنید
3. نام و username ربات را انتخاب کنید
4. Token دریافتی را کپی کنید

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

## 🚀 نحوه استفاده از ربات

### 1️⃣ اضافه کردن ربات به گروه

1. ربات را به گروه اضافه کنید
2. دسترسی ادمین به ربات بدهید (ضروری!)
3. دستور `/setup` را در گروه اجرا کنید

### 2️⃣ تنظیم دسترسی‌های ربات

ربات باید دسترسی‌های زیر را داشته باشد:
- ✅ **Delete messages** - حذف پیام‌ها
- ✅ **Send messages** - ارسال پیام
- ✅ **Read messages** - خواندن پیام‌ها

### 3️⃣ نحوه کار ربات

- **کاربران عادی**: پیام‌هایشان فوراً حذف می‌شود و با نامشان ارسال می‌شود
- **ادمین‌ها**: می‌توانند آزادانه پیام ارسال کنند
- **ضد اسپم**: کاربرانی که بیش از 10 پیام در دقیقه ارسال کنند، 30 دقیقه سکوت می‌شوند

### 4️⃣ مثال استفاده

```
کاربر عادی: "سلام همه!"
ربات: "علی: سلام همه!" (پیام اصلی حذف شده)

ادمین: "خوبید؟"
ربات: (هیچ کاری نمی‌کند - پیام ادمین باقی می‌ماند)
```

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

## 🔐 راهنمای امنیت

### تنظیم امن Token

1. **ایجاد فایل `.env`:**
   ```bash
   # فایل .env (این فایل را در Git قرار ندهید!)
   TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
   DEBUG=True
   TIMEZONE=Asia/Tehran
   ```

2. **تأیید `.gitignore`:**
   ```bash
   # فایل .gitignore باید شامل این خط باشد:
   .env
   ```

3. **تست امنیت:**
   ```bash
   # بررسی کنید که token در کد نیست
   grep -r "YOUR_BOT_TOKEN_HERE" .
   # باید فقط در config.py باشد
   ```

### نکات مهم امنیتی

- ✅ **درست**: Token در فایل `.env`
- ❌ **غلط**: Token در فایل `config.py`
- ✅ **درست**: فایل `.env` در `.gitignore`
- ❌ **غلط**: فایل `.env` در Git

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
- بررسی کنید ربات در گروه است

#### ❌ خطای "InvalidToken"
- Token ربات را بررسی کنید
- مطمئن شوید token در `config.py` یا `.env` درست قرار گرفته
- Token را از [@BotFather](https://t.me/botfather) دوباره دریافت کنید

#### ❌ خطای "Bot was blocked by the user"
- کاربر ربات را بلاک کرده است
- این خطا طبیعی است و ربات به کار خود ادامه می‌دهد

#### ❌ خطای اتصال
- اتصال اینترنت را بررسی کنید
- Token ربات را بررسی کنید
- فایروال سرور را بررسی کنید

#### ❌ خطای Unicode در فایل .env
- فایل `.env` را حذف کنید و دوباره ایجاد کنید
- یا از روش 1 (تنظیم مستقیم در config.py) استفاده کنید

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
   - هرگز token را در کد قرار ندهید
   - از فایل `.env` استفاده کنید
   - فایل `.env` را در `.gitignore` قرار دهید
2. **از HTTPS استفاده کنید**
3. **فایروال سرور را تنظیم کنید**
4. **به‌روزرسانی‌های امنیتی را نصب کنید**
5. **دسترسی‌های فایل‌ها را محدود کنید**
   ```bash
   chmod 600 .env
   chmod 644 config.py
   ```

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

## ❓ سوالات متداول (FAQ)

### سوال: چرا ربات پیام‌های من را حذف می‌کند؟
**پاسخ**: ربات برای گروه‌هایی طراحی شده که فقط ادمین‌ها اجازه ارسال پیام دارند. اگر ادمین نیستید، پیام‌هایتان حذف و با نامتان ارسال می‌شود.

### سوال: چطور ادمین شوم؟
**پاسخ**: فقط مالک گروه می‌تواند شما را ادمین کند. از مالک گروه بخواهید شما را ادمین کند.

### سوال: ربات چطور ادمین‌ها را تشخیص می‌دهد؟
**پاسخ**: ربات با دستور `/setup` لیست ادمین‌ها را از تلگرام دریافت می‌کند.

### سوال: چرا ربات کار نمی‌کند؟
**پاسخ**: 
1. بررسی کنید ربات ادمین است
2. دستور `/setup` را اجرا کنید
3. Token ربات را بررسی کنید

### سوال: چطور ربات را از گروه حذف کنم؟
**پاسخ**: ربات را از گروه remove کنید یا دسترسی ادمین را از آن بگیرید.

## 📞 پشتیبانی

- 📱 **تلگرام**: [@Darius_nake](https://t.me/Darius_nake)
- 🐛 **گزارش باگ**: [Issues](https://github.com/yourusername/admin-group-bot/issues)
- 💡 **پیشنهاد ویژگی**: [Discussions](https://github.com/yourusername/admin-group-bot/discussions)

## ⭐ ستاره دادن

اگر این پروژه برای شما مفید بود، لطفاً یک ستاره ⭐ بدهید!

---

**نکته**: این ربات برای مدیریت گروه‌های تلگرام طراحی شده که فقط ادمین‌ها اجازه ارسال پیام دارند. قبل از استفاده، قوانین و مقررات تلگرام را مطالعه کنید.

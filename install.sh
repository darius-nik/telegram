#!/bin/bash

# اسکریپت نصب خودکار ربات تلگرام در ماشین مجازی
# Telegram Bot Auto Installation Script for VM

echo "🤖 Starting Telegram Bot Installation..."
echo "========================================"

# بررسی سیستم عامل
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    echo "❌ Cannot detect OS version"
    exit 1
fi

echo "📋 Detected OS: $OS $VER"

# به‌روزرسانی سیستم
echo "🔄 Updating system packages..."
if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
    sudo apt update && sudo apt upgrade -y
    sudo apt install python3 python3-pip python3-venv git curl -y
elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
    sudo yum update -y
    sudo yum install python3 python3-pip git curl -y
else
    echo "❌ Unsupported OS: $OS"
    exit 1
fi

# ایجاد کاربر مخصوص ربات
echo "👤 Creating bot user..."
if ! id "telegram-bot" &>/dev/null; then
    sudo useradd -m -s /bin/bash telegram-bot
    echo "✅ Bot user created"
else
    echo "ℹ️ Bot user already exists"
fi

# ایجاد پوشه پروژه
echo "📁 Setting up project directory..."
sudo mkdir -p /home/telegram-bot/telegram-bot
sudo chown telegram-bot:telegram-bot /home/telegram-bot/telegram-bot

# کپی فایل‌های پروژه
echo "📂 Copying project files..."
if [ -f "admin_group_bot.py" ]; then
    sudo cp *.py /home/telegram-bot/telegram-bot/
    sudo cp *.txt /home/telegram-bot/telegram-bot/
    sudo cp *.md /home/telegram-bot/telegram-bot/
    sudo chown -R telegram-bot:telegram-bot /home/telegram-bot/telegram-bot
    echo "✅ Project files copied"
else
    echo "❌ Project files not found in current directory"
    echo "Please run this script from the project directory"
    exit 1
fi

# تنظیم محیط مجازی
echo "🐍 Setting up Python virtual environment..."
sudo -u telegram-bot bash -c "
cd /home/telegram-bot/telegram-bot
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
"

# ایجاد فایل سرویس systemd
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/telegram-bot.service > /dev/null <<EOF
[Unit]
Description=Telegram Admin Bot
After=network.target

[Service]
Type=simple
User=telegram-bot
WorkingDirectory=/home/telegram-bot/telegram-bot
Environment=PATH=/home/telegram-bot/telegram-bot/venv/bin
ExecStart=/home/telegram-bot/telegram-bot/venv/bin/python start_admin_bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# بارگذاری سرویس
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot

# تنظیم مجوزهای فایل‌ها
echo "🔒 Setting file permissions..."
sudo chmod 600 /home/telegram-bot/telegram-bot/config.py
sudo chmod +x /home/telegram-bot/telegram-bot/start_admin_bot.py

# ایجاد اسکریپت مدیریت
echo "📝 Creating management scripts..."
sudo tee /home/telegram-bot/telegram-bot/manage.sh > /dev/null <<'EOF'
#!/bin/bash

case "$1" in
    start)
        echo "🚀 Starting Telegram Bot..."
        sudo systemctl start telegram-bot
        ;;
    stop)
        echo "⏹️ Stopping Telegram Bot..."
        sudo systemctl stop telegram-bot
        ;;
    restart)
        echo "🔄 Restarting Telegram Bot..."
        sudo systemctl restart telegram-bot
        ;;
    status)
        echo "📊 Bot Status:"
        sudo systemctl status telegram-bot
        ;;
    logs)
        echo "📋 Bot Logs:"
        sudo journalctl -u telegram-bot -f
        ;;
    update)
        echo "🔄 Updating bot..."
        sudo systemctl stop telegram-bot
        sudo -u telegram-bot bash -c "
        cd /home/telegram-bot/telegram-bot
        source venv/bin/activate
        pip install --upgrade -r requirements.txt
        "
        sudo systemctl start telegram-bot
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|update}"
        exit 1
        ;;
esac
EOF

sudo chmod +x /home/telegram-bot/telegram-bot/manage.sh
sudo chown telegram-bot:telegram-bot /home/telegram-bot/telegram-bot/manage.sh

# تنظیم فایروال
echo "🔥 Configuring firewall..."
if command -v ufw &> /dev/null; then
    sudo ufw allow ssh
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw allow out 443/tcp
    sudo ufw allow out 80/tcp
    sudo ufw allow out 8443/tcp
    sudo ufw --force enable
    echo "✅ UFW firewall configured with HTTP/HTTPS access"
elif command -v firewall-cmd &> /dev/null; then
    sudo firewall-cmd --permanent --add-service=ssh
    sudo firewall-cmd --permanent --add-service=http
    sudo firewall-cmd --permanent --add-service=https
    sudo firewall-cmd --reload
    echo "✅ Firewalld configured with HTTP/HTTPS access"
fi

# نمایش اطلاعات نصب
echo ""
echo "🎉 Installation completed successfully!"
echo "========================================"
echo ""
echo "📋 Next steps:"
echo "1. Edit config.py and add your bot token:"
echo "   sudo nano /home/telegram-bot/telegram-bot/config.py"
echo ""
echo "2. Start the bot:"
echo "   sudo systemctl start telegram-bot"
echo ""
echo "3. Check status:"
echo "   sudo systemctl status telegram-bot"
echo ""
echo "4. View logs:"
echo "   sudo journalctl -u telegram-bot -f"
echo ""
echo "5. Use management script:"
echo "   /home/telegram-bot/telegram-bot/manage.sh {start|stop|restart|status|logs|update}"
echo ""
echo "🔧 Bot files location: /home/telegram-bot/telegram-bot/"
echo "📊 Service name: telegram-bot"
echo ""
echo "⚠️  Don't forget to add your bot token to config.py!"
echo ""



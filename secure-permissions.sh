#!/bin/bash

# Secure File Permissions Script for Telegram Bot
# This script sets proper file permissions for security

echo "🔒 Setting secure file permissions..."
echo "===================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script as root (use sudo)"
    exit 1
fi

# Get the project directory
PROJECT_DIR=$(pwd)
echo "📁 Project directory: $PROJECT_DIR"

# Create necessary directories
echo "📂 Creating necessary directories..."
mkdir -p data logs ssl
mkdir -p logs/nginx

# Set ownership to bot user (create if doesn't exist)
BOT_USER="telegram-bot"
if ! id "$BOT_USER" &>/dev/null; then
    echo "👤 Creating bot user: $BOT_USER"
    useradd -r -s /bin/false -d "$PROJECT_DIR" "$BOT_USER"
fi

# Set ownership of project directory
echo "👤 Setting ownership to bot user..."
chown -R "$BOT_USER:$BOT_USER" "$PROJECT_DIR"

# Set secure permissions for different file types
echo "🔐 Setting secure file permissions..."

# Configuration files - read only for owner
chmod 600 .env 2>/dev/null || echo "⚠️ .env file not found (will be created later)"
chmod 600 config.py
chmod 600 nginx.conf
chmod 600 docker-compose.yml

# Scripts - executable for owner only
chmod 700 *.sh 2>/dev/null || echo "ℹ️ No shell scripts found"
chmod 700 install.sh
chmod 700 setup-firewall.sh
chmod 700 secure-permissions.sh

# Python files - read and execute for owner
chmod 700 *.py
chmod 700 admin_group_bot.py
chmod 700 start_admin_bot.py
chmod 700 test_admin_bot.py

# Data and logs directories - read/write for owner only
chmod 700 data logs
chmod 700 logs/nginx

# SSL directory - read only for owner
chmod 700 ssl

# Requirements and documentation - read only
chmod 644 requirements.txt
chmod 644 README.md
chmod 644 LICENSE
chmod 644 Dockerfile

# Database file - read/write for owner only
chmod 600 telegram_bot.db 2>/dev/null || echo "ℹ️ Database file not found (will be created later)"

# Log files - read/write for owner only
chmod 600 bot.log 2>/dev/null || echo "ℹ️ Log file not found (will be created later)"

# Remove world and group permissions from sensitive files
echo "🚫 Removing world and group permissions from sensitive files..."
find "$PROJECT_DIR" -name "*.env*" -exec chmod 600 {} \; 2>/dev/null
find "$PROJECT_DIR" -name "*.log" -exec chmod 600 {} \; 2>/dev/null
find "$PROJECT_DIR" -name "*.db" -exec chmod 600 {} \; 2>/dev/null
find "$PROJECT_DIR" -name "*.conf" -exec chmod 600 {} \; 2>/dev/null
find "$PROJECT_DIR" -name "*.key" -exec chmod 600 {} \; 2>/dev/null
find "$PROJECT_DIR" -name "*.pem" -exec chmod 600 {} \; 2>/dev/null

# Set sticky bit on directories to prevent deletion
echo "🔒 Setting sticky bit on directories..."
chmod +t data logs ssl logs/nginx

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo "📝 Creating .gitignore file..."
    cat > .gitignore << 'EOF'
# Environment files
.env
.env.local
.env.production

# Logs
*.log
logs/
bot.log

# Database files
*.db
*.sqlite
*.sqlite3

# SSL certificates
ssl/
*.pem
*.key
*.crt

# Data directory
data/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so

# Virtual environment
venv/
env/
ENV/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Docker
.dockerignore
EOF
    chmod 644 .gitignore
fi

# Set proper permissions for .gitignore
chmod 644 .gitignore

# Create a secure .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating secure .env file from template..."
    cp env.example .env
    chmod 600 .env
    chown "$BOT_USER:$BOT_USER" .env
    echo "⚠️ IMPORTANT: Edit .env file and add your actual bot token!"
fi

# Summary
echo ""
echo "✅ File permissions set successfully!"
echo "===================================="
echo ""
echo "📋 Permission summary:"
echo "• Configuration files: 600 (owner read/write only)"
echo "• Scripts: 700 (owner read/write/execute only)"
echo "• Python files: 700 (owner read/write/execute only)"
echo "• Data/logs directories: 700 (owner read/write/execute only)"
echo "• Documentation: 644 (owner read/write, group/other read only)"
echo "• Sensitive files: 600 (owner read/write only)"
echo ""
echo "👤 Owner: $BOT_USER"
echo "📁 Project directory: $PROJECT_DIR"
echo ""
echo "🔒 Security features applied:"
echo "• No world/group permissions on sensitive files"
echo "• Sticky bit on directories"
echo "• Proper ownership for bot user"
echo "• Secure .gitignore file"
echo ""
echo "⚠️ Next steps:"
echo "1. Edit .env file with your actual bot token"
echo "2. Test the bot with: python test_admin_bot.py"
echo "3. Run the bot with: python start_admin_bot.py"
echo ""
echo "🔍 To check permissions: ls -la"
echo "🔍 To check ownership: ls -la | grep $BOT_USER"

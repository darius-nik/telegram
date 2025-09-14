#!/bin/bash

# Fail2ban Configuration Script for Telegram Bot Server
# This script installs and configures fail2ban for additional security

echo "🛡️ Setting up Fail2ban for enhanced security..."
echo "=============================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script as root (use sudo)"
    exit 1
fi

# Check if fail2ban is installed
if ! command -v fail2ban-client &> /dev/null; then
    echo "📦 Installing Fail2ban..."
    apt update && apt install -y fail2ban
fi

# Create fail2ban configuration
echo "📝 Creating Fail2ban configuration..."
cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
# Ban hosts for one hour:
bantime = 3600

# Override /etc/fail2ban/jail.d/00-firewalld.conf:
banaction = ufw

# A host is banned if it has generated "maxretry" during "findtime" seconds:
findtime = 600
maxretry = 3

# Destination email address used solely for the interpolations in
# jail.{conf,local,d/*} configuration files.
destemail = root@localhost

# Sender email address used solely for some actions
sender = root@localhost

# Default action
action = %(action_mwl)s

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3
bantime = 3600
findtime = 600

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3
bantime = 3600
findtime = 600

[nginx-bot-requests]
enabled = true
filter = nginx-bot-requests
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 10
bantime = 1800
findtime = 300
EOF

# Create custom filter for bot requests
echo "🔍 Creating custom filter for bot requests..."
cat > /etc/fail2ban/filter.d/nginx-bot-requests.conf << 'EOF'
[Definition]
failregex = ^<HOST> -.*"(GET|POST) /webhook.*" (4\d\d|5\d\d) .*$
            ^<HOST> -.*"(GET|POST) /.*" (4\d\d|5\d\d) .*$
ignoreregex =
EOF

# Create custom filter for nginx limit req
echo "🔍 Creating custom filter for nginx limit requests..."
cat > /etc/fail2ban/filter.d/nginx-limit-req.conf << 'EOF'
[Definition]
failregex = limiting requests, excess: .* by zone .*, client: <HOST>
ignoreregex =
EOF

# Set proper permissions
echo "🔐 Setting proper permissions..."
chmod 644 /etc/fail2ban/jail.local
chmod 644 /etc/fail2ban/filter.d/nginx-bot-requests.conf
chmod 644 /etc/fail2ban/filter.d/nginx-limit-req.conf

# Enable and start fail2ban
echo "🚀 Enabling and starting Fail2ban..."
systemctl enable fail2ban
systemctl restart fail2ban

# Check status
echo "📊 Checking Fail2ban status..."
systemctl status fail2ban --no-pager -l

echo ""
echo "✅ Fail2ban setup completed!"
echo "=========================="
echo ""
echo "📋 Configuration summary:"
echo "• SSH protection: 3 failed attempts = 1 hour ban"
echo "• Nginx HTTP auth protection: 3 failed attempts = 1 hour ban"
echo "• Nginx rate limiting protection: 3 failed attempts = 1 hour ban"
echo "• Bot request protection: 10 failed attempts = 30 minutes ban"
echo ""
echo "🔍 Useful commands:"
echo "• Check status: sudo fail2ban-client status"
echo "• Check specific jail: sudo fail2ban-client status sshd"
echo "• Unban IP: sudo fail2ban-client set sshd unbanip <IP>"
echo "• View logs: sudo tail -f /var/log/fail2ban.log"
echo ""
echo "⚠️ Important notes:"
echo "• Make sure you can still SSH to the server!"
echo "• Test your connection before closing this session"
echo "• If you get locked out, you may need to access via console"
echo "• Fail2ban logs are in /var/log/fail2ban.log"
echo ""
echo "🎉 Enhanced security setup completed!"

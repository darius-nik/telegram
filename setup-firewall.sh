#!/bin/bash

# Secure Firewall Configuration Script for Telegram Bot Server
# This script configures UFW (Ubuntu Firewall) with secure rules

echo "🔥 Setting up secure firewall configuration..."
echo "=============================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script as root (use sudo)"
    exit 1
fi

# Check if UFW is installed
if ! command -v ufw &> /dev/null; then
    echo "📦 Installing UFW firewall..."
    apt update && apt install -y ufw
fi

# Reset UFW to default state
echo "🔄 Resetting UFW to default state..."
ufw --force reset

# Set default policies
echo "🛡️ Setting default firewall policies..."
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (be very careful with this!)
echo "🔐 Configuring SSH access..."
read -p "Enter your SSH port (default: 22): " ssh_port
ssh_port=${ssh_port:-22}

# Validate SSH port
if ! [[ "$ssh_port" =~ ^[0-9]+$ ]] || [ "$ssh_port" -lt 1 ] || [ "$ssh_port" -gt 65535 ]; then
    echo "❌ Invalid SSH port. Using default port 22."
    ssh_port=22
fi

# Allow SSH from specific IP (recommended for production)
read -p "Do you want to restrict SSH to specific IP? (y/n): " restrict_ssh
if [ "$restrict_ssh" = "y" ] || [ "$restrict_ssh" = "Y" ]; then
    read -p "Enter your IP address (or CIDR like 192.168.1.0/24): " user_ip
    # Improved IP validation - supports both single IP and CIDR
    if [[ $user_ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(/[0-9]{1,2})?$ ]]; then
        ufw allow from $user_ip to any port $ssh_port
        echo "✅ SSH access allowed only from $user_ip on port $ssh_port"
    else
        echo "❌ Invalid IP address format. Allowing SSH from anywhere (NOT RECOMMENDED for production!)"
        ufw allow $ssh_port
    fi
else
    echo "⚠️ WARNING: Allowing SSH from anywhere (NOT RECOMMENDED for production!)"
    ufw allow $ssh_port
fi

# Allow HTTP and HTTPS
echo "🌐 Configuring web access..."
ufw allow 80/tcp
ufw allow 443/tcp
echo "✅ HTTP (80) and HTTPS (443) access allowed"

# Allow Telegram Bot API (outbound)
echo "🤖 Configuring Telegram Bot API access..."
ufw allow out 443/tcp
ufw allow out 80/tcp
ufw allow out 8443/tcp
echo "✅ Outbound HTTPS/HTTP/Webhook access allowed for Telegram API"

# Optional: Allow specific services
echo ""
echo "🔧 Optional services configuration:"
read -p "Do you want to allow DNS queries? (y/n): " allow_dns
if [ "$allow_dns" = "y" ] || [ "$allow_dns" = "Y" ]; then
    ufw allow out 53/udp
    ufw allow out 53/tcp
    echo "✅ DNS queries allowed"
fi

read -p "Do you want to allow NTP time sync? (y/n): " allow_ntp
if [ "$allow_ntp" = "y" ] || [ "$allow_ntp" = "Y" ]; then
    ufw allow out 123/udp
    echo "✅ NTP time sync allowed"
fi

# Rate limiting for SSH (more permissive)
echo "⚡ Configuring rate limiting for SSH..."
ufw limit $ssh_port/tcp
echo "✅ SSH rate limiting enabled (6 connections per 30 seconds)"

# Enable logging
echo "📝 Enabling firewall logging..."
ufw logging on
echo "✅ Firewall logging enabled"

# Show configuration before enabling
echo ""
echo "📋 Firewall configuration summary:"
echo "=================================="
ufw show added

echo ""
read -p "Do you want to enable the firewall now? (y/n): " enable_firewall
if [ "$enable_firewall" = "y" ] || [ "$enable_firewall" = "Y" ]; then
    echo "🚀 Enabling firewall..."
    ufw --force enable
    echo "✅ Firewall enabled successfully!"
    
    echo ""
    echo "📊 Current firewall status:"
    ufw status verbose
    
    echo ""
    echo "⚠️ IMPORTANT SECURITY NOTES:"
    echo "============================"
    echo "1. Make sure you can still SSH to the server!"
    echo "2. Test your connection before closing this session"
    echo "3. If you get locked out, you may need to access via console"
    echo "4. Firewall logs are in /var/log/ufw.log"
    echo "5. To disable firewall: sudo ufw disable"
    echo "6. To check status: sudo ufw status verbose"
    
else
    echo "ℹ️ Firewall configured but not enabled yet."
    echo "To enable later, run: sudo ufw enable"
fi

echo ""
echo "🔒 Additional security recommendations:"
echo "======================================"
echo "1. Change default SSH port (edit /etc/ssh/sshd_config)"
echo "2. Disable root login (PermitRootLogin no)"
echo "3. Use SSH keys instead of passwords"
echo "4. Enable fail2ban for additional protection"
echo "5. Keep system updated: apt update && apt upgrade"
echo "6. Monitor logs regularly: tail -f /var/log/ufw.log"

echo ""
echo "🎉 Firewall setup completed!"

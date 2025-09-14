#!/bin/bash

# SSL Certificate Generation Script for Telegram Bot
# This script generates self-signed SSL certificates for development/testing

echo "🔐 Generating SSL certificates..."
echo "================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script as root (use sudo)"
    exit 1
fi

# Create SSL directory
echo "📁 Creating SSL directory..."
mkdir -p ssl
chmod 700 ssl

# Generate private key
echo "🔑 Generating private key..."
openssl genrsa -out ssl/key.pem 2048
chmod 600 ssl/key.pem

# Generate certificate signing request
echo "📝 Generating certificate signing request..."
openssl req -new -key ssl/key.pem -out ssl/cert.csr -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Generate self-signed certificate
echo "📜 Generating self-signed certificate..."
openssl x509 -req -days 365 -in ssl/cert.csr -signkey ssl/key.pem -out ssl/cert.pem
chmod 644 ssl/cert.pem

# Clean up CSR file
rm ssl/cert.csr

# Set proper ownership
echo "👤 Setting ownership..."
chown -R 101:101 ssl/

echo ""
echo "✅ SSL certificates generated successfully!"
echo "=========================================="
echo ""
echo "📋 Certificate details:"
echo "• Private key: ssl/key.pem"
echo "• Certificate: ssl/cert.pem"
echo "• Valid for: 365 days"
echo "• Subject: localhost"
echo ""
echo "⚠️ IMPORTANT NOTES:"
echo "=================="
echo "1. These are SELF-SIGNED certificates for development only"
echo "2. Browsers will show security warnings"
echo "3. For production, use certificates from a trusted CA"
echo "4. Consider using Let's Encrypt for free SSL certificates"
echo ""
echo "🔧 To use with Let's Encrypt:"
echo "1. Install certbot: apt install certbot"
echo "2. Get certificate: certbot certonly --standalone -d yourdomain.com"
echo "3. Update nginx.conf with the new certificate paths"
echo ""
echo "📁 Certificate files:"
ls -la ssl/

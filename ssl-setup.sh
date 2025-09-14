#!/bin/bash

# SSL Certificate Setup Script for Telegram Bot
# This script helps you set up SSL certificates for HTTPS

echo "🔐 Setting up SSL certificates..."
echo "================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script as root (use sudo)"
    exit 1
fi

# Create SSL directory
echo "📁 Creating SSL directory..."
mkdir -p ssl
chmod 700 ssl

# Check if certificates already exist
if [ -f "ssl/cert.pem" ] && [ -f "ssl/key.pem" ]; then
    echo "✅ SSL certificates already exist"
    echo "📋 Certificate info:"
    openssl x509 -in ssl/cert.pem -text -noout | grep -E "(Subject:|Not Before|Not After)"
    exit 0
fi

echo ""
echo "🔧 SSL Certificate Options:"
echo "1. Generate self-signed certificate (for testing)"
echo "2. Use Let's Encrypt (for production)"
echo "3. Use existing certificates"
echo "4. Skip SSL setup"
echo ""

read -p "Choose an option (1-4): " ssl_option

case $ssl_option in
    1)
        echo "🔧 Generating self-signed certificate..."
        read -p "Enter domain name (or localhost): " domain
        domain=${domain:-localhost}
        
        openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem \
            -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=$domain"
        
        chmod 600 ssl/key.pem
        chmod 644 ssl/cert.pem
        chown -R 101:101 ssl/  # nginx user
        
        echo "✅ Self-signed certificate generated for $domain"
        echo "⚠️  WARNING: Self-signed certificates are not trusted by browsers"
        ;;
        
    2)
        echo "🔧 Let's Encrypt setup..."
        read -p "Enter your domain name: " domain
        
        if [ -z "$domain" ]; then
            echo "❌ Domain name is required for Let's Encrypt"
            exit 1
        fi
        
        # Install certbot if not installed
        if ! command -v certbot &> /dev/null; then
            echo "📦 Installing certbot..."
            apt update && apt install -y certbot
        fi
        
        # Generate certificate
        echo "🔐 Generating Let's Encrypt certificate..."
        certbot certonly --standalone -d "$domain" --non-interactive --agree-tos \
            --email "admin@$domain" --expand
        
        # Copy certificates to ssl directory
        cp "/etc/letsencrypt/live/$domain/fullchain.pem" ssl/cert.pem
        cp "/etc/letsencrypt/live/$domain/privkey.pem" ssl/key.pem
        
        chmod 600 ssl/key.pem
        chmod 644 ssl/cert.pem
        chown -R 101:101 ssl/  # nginx user
        
        echo "✅ Let's Encrypt certificate generated for $domain"
        echo "🔄 Setting up auto-renewal..."
        
        # Add renewal script
        cat > /etc/cron.d/certbot-renewal << EOF
# Renew Let's Encrypt certificates
0 12 * * * root certbot renew --quiet --post-hook "cp /etc/letsencrypt/live/$domain/fullchain.pem $PWD/ssl/cert.pem && cp /etc/letsencrypt/live/$domain/privkey.pem $PWD/ssl/key.pem && chmod 600 $PWD/ssl/key.pem && chmod 644 $PWD/ssl/cert.pem && chown -R 101:101 $PWD/ssl/ && docker-compose restart nginx"
EOF
        
        echo "✅ Auto-renewal configured"
        ;;
        
    3)
        echo "🔧 Using existing certificates..."
        read -p "Enter path to certificate file: " cert_path
        read -p "Enter path to private key file: " key_path
        
        if [ ! -f "$cert_path" ] || [ ! -f "$key_path" ]; then
            echo "❌ Certificate files not found"
            exit 1
        fi
        
        cp "$cert_path" ssl/cert.pem
        cp "$key_path" ssl/key.pem
        
        chmod 600 ssl/key.pem
        chmod 644 ssl/cert.pem
        chown -R 101:101 ssl/  # nginx user
        
        echo "✅ Existing certificates copied"
        ;;
        
    4)
        echo "⏭️  Skipping SSL setup"
        echo "⚠️  WARNING: HTTPS will not work without SSL certificates"
        exit 0
        ;;
        
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "📋 SSL Setup Summary:"
echo "====================="
echo "• Certificate: ssl/cert.pem"
echo "• Private Key: ssl/key.pem"
echo "• Permissions: 644 (cert), 600 (key)"
echo "• Owner: nginx user (101:101)"
echo ""

if [ -f "ssl/cert.pem" ] && [ -f "ssl/key.pem" ]; then
    echo "🔍 Certificate Details:"
    openssl x509 -in ssl/cert.pem -text -noout | grep -E "(Subject:|Not Before|Not After|Issuer:)"
    echo ""
    echo "✅ SSL setup completed successfully!"
    echo "🚀 You can now start the bot with HTTPS support"
else
    echo "❌ SSL setup failed"
    exit 1
fi

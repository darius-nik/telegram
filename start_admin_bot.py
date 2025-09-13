#!/usr/bin/env python3
"""
Startup script for Admin Group Bot
This script starts the admin group management bot
"""

import sys
import os
import logging

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from admin_group_bot import AdminGroupBot
    from config import Config
    
    def main():
        """Main function to start the bot"""
        print("🤖 Starting Admin Group Bot...")
        print("📋 Bot Features:")
        print("   • Admin-only group management")
        print("   • Automatic message deletion for non-admins")
        print("   • Message reposting with username format")
        print("   • Real-time admin list management")
        print("=" * 50)
        
        # Check bot token
        if not Config.TELEGRAM_BOT_TOKEN or Config.TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
            print("❌ Error: Bot token not configured!")
            print("Please set your bot token in config.py")
            sys.exit(1)
        
        print(f"✅ Bot token configured: {Config.TELEGRAM_BOT_TOKEN[:10]}...")
        print("🚀 Starting bot...")
        print("📝 Logs will be shown below:")
        print("=" * 50)
        
        try:
            bot = AdminGroupBot()
            bot.run()
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
        except Exception as e:
            print(f"❌ Error starting bot: {e}")
            logging.error(f"Error starting bot: {e}")
            print("\n🔍 Troubleshooting tips:")
            print("1. Check your bot token in config.py")
            print("2. Make sure you have internet connection")
            print("3. Run: python test_admin_bot.py")
            sys.exit(1)
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure all required packages are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)

#!/usr/bin/env python3
"""
Test script for Admin Group Bot
This script helps diagnose setup issues
"""

import asyncio
import logging
from telegram import Bot
from telegram.error import TelegramError
from config import Config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def test_bot_connection():
    """Test bot connection and basic functionality"""
    try:
        bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        
        # Get bot info
        bot_info = await bot.get_me()
        logger.info(f"Bot connected successfully: @{bot_info.username}")
        
        return True
    except Exception as e:
        logger.error(f"Bot connection failed: {e}")
        return False

async def test_chat_permissions(chat_id: int):
    """Test bot permissions in a specific chat"""
    try:
        bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        
        # Get chat info
        chat = await bot.get_chat(chat_id)
        logger.info(f"Chat info: {chat.title} (type: {chat.type})")
        
        # Get bot member info
        bot_member = await bot.get_chat_member(chat_id, bot.id)
        logger.info(f"Bot status: {bot_member.status}")
        
        # Get chat administrators
        admins = await bot.get_chat_administrators(chat_id)
        logger.info(f"Found {len(admins)} administrators")
        
        for admin in admins:
            logger.info(f"Admin: {admin.user.first_name} (@{admin.user.username}) - {admin.status}")
        
        return True
    except TelegramError as e:
        logger.error(f"Error testing chat permissions: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

async def main():
    """Main test function"""
    print("🔍 Testing Admin Group Bot...")
    print("=" * 50)
    
    # Test bot connection
    print("1. Testing bot connection...")
    if await test_bot_connection():
        print("✅ Bot connection successful")
    else:
        print("❌ Bot connection failed")
        return
    
    # Test chat permissions (you need to provide a chat ID)
    print("\n2. Testing chat permissions...")
    print("To test chat permissions, please provide a chat ID.")
    print("You can get chat ID by adding @userinfobot to your group.")
    
    chat_id = input("Enter chat ID (or press Enter to skip): ").strip()
    if chat_id:
        try:
            chat_id = int(chat_id)
            if await test_chat_permissions(chat_id):
                print("✅ Chat permissions test successful")
            else:
                print("❌ Chat permissions test failed")
        except ValueError:
            print("❌ Invalid chat ID format")

if __name__ == "__main__":
    asyncio.run(main())

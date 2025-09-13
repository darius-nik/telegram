import logging
import asyncio
from datetime import datetime
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode, ChatMemberStatus
from telegram.error import TelegramError
import os

from config import Config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class AdminGroupBot:
    def __init__(self):
        # Create application with optimized settings
        self.application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        
        # Add handlers
        self._add_handlers()
        
        # Store admin users for each group
        self.group_admins = {}
        
        # Queue system to prevent conflicts
        self.processing_queues = {}  # chat_id -> asyncio.Queue
        self.processing_locks = {}  # chat_id -> asyncio.Lock
        
        # Performance optimization: user name cache
        self.user_name_cache = {}  # user_id -> name
        
        # Anti-spam system
        self.user_message_times = {}  # (chat_id, user_id) -> list of message times
        self.muted_users = {}  # (chat_id, user_id) -> mute_until_time
        self.spam_mode_enabled = {}  # chat_id -> bool (whether spam detection is enabled for admins)
    
    def _add_handlers(self):
        """Add all command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("setup", self.setup_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("refresh_admins", self.refresh_admins_command))
        self.application.add_handler(CommandHandler("unmute", self.unmute_command))
        self.application.add_handler(CommandHandler("spam_mode", self.spam_mode_command))
        
        # Message handlers - handle all messages in groups (text, stickers, media, etc.)
        self.application.add_handler(MessageHandler(
            filters.ChatType.GROUPS & ~filters.COMMAND, 
            self.handle_group_message
        ))
        
        # Handle new chat members
        self.application.add_handler(MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            self.handle_new_chat_members
        ))
        
        # Handle left chat members
        self.application.add_handler(MessageHandler(
            filters.StatusUpdate.LEFT_CHAT_MEMBER,
            self.handle_left_chat_member
        ))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        chat_type = update.effective_chat.type
        
        if chat_type == "private":
            await update.message.reply_text(
                "🤖 <b>ربات مدیریت گروه ادمین</b>\n\n"
                "این ربات برای مدیریت گروه‌هایی طراحی شده که فقط ادمین‌ها اجازه ارسال پیام دارند.\n\n"
                "📋 <b>قابلیت‌ها:</b>\n"
                "• حذف خودکار پیام‌های کاربران عادی\n"
                "• ارسال مجدد پیام با نام کاربر\n"
                "• مدیریت دسترسی‌های گروه\n\n"
                "برای استفاده:\n"
                "1. ربات را به گروه اضافه کنید\n"
                "2. دسترسی ادمین به ربات بدهید\n"
                "3. دستور /setup را در گروه اجرا کنید\n\n"
                "برای راهنما: /help",
                parse_mode=ParseMode.HTML
            )
        else:
            await update.message.reply_text(
                "🤖 ربات مدیریت گروه فعال شد!\n\n"
                "برای راهنما: /help\n"
                "برای تنظیم: /setup",
                parse_mode=ParseMode.HTML
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📖 <b>راهنمای ربات مدیریت گروه ادمین</b>

🔧 <b>دستورات:</b>
/setup - تنظیم ربات در گروه
/status - وضعیت ربات و لیست ادمین‌ها
/refresh_admins - بروزرسانی لیست ادمین‌ها
/help - نمایش این راهنما

⚙️ <b>نحوه کار:</b>
1. ربات را به گروه اضافه کنید
2. دسترسی ادمین به ربات بدهید
3. دستور /setup را اجرا کنید
4. ربات شروع به حذف پیام‌های کاربران عادی می‌کند
5. پیام‌های حذف شده با نام کاربر ارسال می‌شوند

👥 <b>نکات مهم:</b>
• فقط ادمین‌های گروه می‌توانند پیام ارسال کنند
• پیام‌های کاربران عادی فوراً حذف می‌شوند
• پیام‌های حذف شده با فرمت "نام کاربر: متن پیام" ارسال می‌شوند
• ربات باید دسترسی ادمین داشته باشد

🛠️ <b>مشکلات احتمالی:</b>
• اگر ربات پیام‌ها را حذف نمی‌کند، دسترسی ادمین را بررسی کنید
• برای بروزرسانی لیست ادمین‌ها از /refresh_admins استفاده کنید
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)
    
    async def setup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Setup bot in the group"""
        chat = update.effective_chat
        user = update.effective_user
        
        logger.info(f"Setup command called by user {user.id} in chat {chat.id} (type: {chat.type})")
        
        # Check if it's a group
        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text(
                "❌ این دستور فقط در گروه‌ها قابل استفاده است."
            )
            return
        
        # Check if user is admin
        try:
            chat_member = await context.bot.get_chat_member(chat.id, user.id)
            logger.info(f"User {user.id} status: {chat_member.status}")
            
            if chat_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                await update.message.reply_text(
                    "❌ فقط ادمین‌های گروه می‌توانند این دستور را اجرا کنند."
                )
                return
        except TelegramError as e:
            logger.error(f"Error checking admin status: {e}")
            await update.message.reply_text(
                "❌ خطا در بررسی دسترسی‌ها. لطفاً مطمئن شوید ربات دسترسی ادمین دارد."
            )
            return
        
        # Check if bot is admin
        try:
            bot_member = await context.bot.get_chat_member(chat.id, context.bot.id)
            logger.info(f"Bot status: {bot_member.status}")
            
            if bot_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                await update.message.reply_text(
                    "❌ ربات باید دسترسی ادمین داشته باشد تا بتواند پیام‌ها را حذف کند.\n\n"
                    "لطفاً دسترسی ادمین به ربات بدهید و دوباره تلاش کنید.\n\n"
                    "📋 <b>دسترسی‌های مورد نیاز:</b>\n"
                    "• Delete messages\n"
                    "• Send messages\n"
                    "• Read messages",
                    parse_mode=ParseMode.HTML
                )
                return
        except TelegramError as e:
            logger.error(f"Error checking bot admin status: {e}")
            await update.message.reply_text(
                "❌ خطا در بررسی دسترسی ربات. لطفاً مطمئن شوید ربات دسترسی ادمین دارد."
            )
            return
        
        # Refresh admin list
        try:
            await self._refresh_group_admins(chat.id, context)
            admin_count = len(self.group_admins.get(chat.id, []))
            logger.info(f"Refreshed admins for chat {chat.id}: {admin_count} admins")
            
            await update.message.reply_text(
                f"✅ <b>ربات با موفقیت تنظیم شد!</b>\n\n"
                f"📊 تعداد ادمین‌های شناسایی شده: {admin_count}\n\n"
                f"🔧 <b>وضعیت:</b>\n"
                f"• حذف خودکار پیام‌های کاربران عادی: فعال\n"
                f"• ارسال مجدد پیام‌ها: فعال\n\n"
                f"برای مشاهده وضعیت: /status\n"
                f"برای بروزرسانی ادمین‌ها: /refresh_admins",
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Error in setup: {e}")
            await update.message.reply_text(
                "❌ خطا در تنظیم ربات. لطفاً دوباره تلاش کنید."
            )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show bot status and admin list"""
        chat = update.effective_chat
        user = update.effective_user
        
        # Check if it's a group
        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text(
                "❌ این دستور فقط در گروه‌ها قابل استفاده است."
            )
            return
        
        # Check if user is admin
        try:
            chat_member = await context.bot.get_chat_member(chat.id, user.id)
            if chat_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                await update.message.reply_text(
                    "❌ فقط ادمین‌های گروه می‌توانند این دستور را اجرا کنند."
                )
                return
        except TelegramError as e:
            logger.error(f"Error checking admin status: {e}")
            return
        
        # Get admin list
        admins = self.group_admins.get(chat.id, [])
        
        if not admins:
            await update.message.reply_text(
                "⚠️ <b>وضعیت ربات</b>\n\n"
                "❌ لیست ادمین‌ها خالی است.\n"
                "لطفاً دستور /refresh_admins را اجرا کنید.",
                parse_mode=ParseMode.HTML
            )
            return
        
        # Format admin list
        admin_list = []
        for admin_id in admins:
            try:
                admin_member = await context.bot.get_chat_member(chat.id, admin_id)
                admin_name = admin_member.user.first_name or "نامشخص"
                if admin_member.user.username:
                    admin_name += f" (@{admin_member.user.username})"
                admin_list.append(f"• {admin_name}")
            except TelegramError:
                admin_list.append(f"• کاربر {admin_id} (نامشخص)")
        
        status_text = f"""
📊 <b>وضعیت ربات</b>

✅ <b>وضعیت:</b> فعال
👥 <b>تعداد ادمین‌ها:</b> {len(admins)}
🔧 <b>حذف خودکار:</b> فعال
📝 <b>ارسال مجدد:</b> فعال

👑 <b>لیست ادمین‌ها:</b>
{chr(10).join(admin_list)}

🔄 برای بروزرسانی: /refresh_admins
        """
        
        await update.message.reply_text(status_text, parse_mode=ParseMode.HTML)
    
    async def refresh_admins_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Refresh admin list for the group"""
        chat = update.effective_chat
        user = update.effective_user
        
        # Check if it's a group
        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text(
                "❌ این دستور فقط در گروه‌ها قابل استفاده است."
            )
            return
        
        # Check if user is admin
        try:
            chat_member = await context.bot.get_chat_member(chat.id, user.id)
            if chat_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                await update.message.reply_text(
                    "❌ فقط ادمین‌های گروه می‌توانند این دستور را اجرا کنند."
                )
                return
        except TelegramError as e:
            logger.error(f"Error checking admin status: {e}")
            return
        
        # Refresh admin list
        old_count = len(self.group_admins.get(chat.id, []))
        await self._refresh_group_admins(chat.id, context)
        new_count = len(self.group_admins.get(chat.id, []))
        
        await update.message.reply_text(
            f"🔄 <b>لیست ادمین‌ها بروزرسانی شد!</b>\n\n"
            f"📊 تعداد قبلی: {old_count}\n"
            f"📊 تعداد جدید: {new_count}\n\n"
            f"✅ بروزرسانی با موفقیت انجام شد.",
            parse_mode=ParseMode.HTML
        )
    
    async def _refresh_group_admins(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
        """Refresh admin list for a specific group"""
        try:
            admins = await context.bot.get_chat_administrators(chat_id)
            admin_ids = []
            
            for admin in admins:
                if admin.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                    admin_ids.append(admin.user.id)
            
            self.group_admins[chat_id] = admin_ids
            logger.info(f"Refreshed admins for chat {chat_id}: {len(admin_ids)} admins")
            
        except TelegramError as e:
            logger.error(f"Error refreshing admins for chat {chat_id}: {e}")
            self.group_admins[chat_id] = []
    
    async def unmute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Unmute a user (admin only)"""
        chat = update.effective_chat
        user = update.effective_user
        
        # Check if in group
        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text("❌ این دستور فقط در گروه‌ها قابل استفاده است!")
            return
        
        # Check if user is admin
        if user.id not in self.group_admins.get(chat.id, []):
            await update.message.reply_text("❌ فقط ادمین‌ها می‌توانند از این دستور استفاده کنند!")
            return
        
        # Check if user replied to a message
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ لطفاً روی پیام کاربری که می‌خواهید از سکوت دربیاورید ریپلای کنید!")
            return
        
        target_user = update.message.reply_to_message.from_user
        mute_key = (chat.id, target_user.id)
        
        # Check if user is muted
        if mute_key in self.muted_users:
            del self.muted_users[mute_key]
            # Also clear message history
            message_key = (chat.id, target_user.id)
            if message_key in self.user_message_times:
                del self.user_message_times[message_key]
            
            await update.message.reply_text(f"✅ کاربر <b>{target_user.first_name or 'کاربر'}</b> از سکوت درآمد!",
                                          parse_mode=ParseMode.HTML)
            logger.info(f"User {target_user.id} unmuted by admin {user.id} in chat {chat.id}")
        else:
            await update.message.reply_text(f"❌ کاربر <b>{target_user.first_name or 'کاربر'}</b> در حال حاضر سکوت نیست!",
                                          parse_mode=ParseMode.HTML)
    
    async def spam_mode_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Toggle spam detection for admins (admin only)"""
        chat = update.effective_chat
        user = update.effective_user
        
        # Check if in group
        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text("❌ این دستور فقط در گروه‌ها قابل استفاده است!")
            return
        
        # Check if user is admin
        if user.id not in self.group_admins.get(chat.id, []):
            await update.message.reply_text("❌ فقط ادمین‌ها می‌توانند از این دستور استفاده کنند!")
            return
        
        # Toggle spam mode
        current_mode = self.spam_mode_enabled.get(chat.id, False)
        self.spam_mode_enabled[chat.id] = not current_mode
        new_mode = self.spam_mode_enabled[chat.id]
        
        if new_mode:
            await update.message.reply_text(
                "🛡️ <b>حالت ضد اسپم برای ادمین‌ها فعال شد!</b>\n\n"
                "✅ حالا ادمین‌ها هم در صورت اسپم سکوت می‌شوند\n"
                "⚠️ برای غیرفعال کردن دوباره این دستور را بزنید",
                parse_mode=ParseMode.HTML
            )
            logger.info(f"Spam mode enabled for admins in chat {chat.id} by user {user.id}")
        else:
            await update.message.reply_text(
                "🔓 <b>حالت ضد اسپم برای ادمین‌ها غیرفعال شد!</b>\n\n"
                "✅ ادمین‌ها دیگر سکوت نمی‌شوند\n"
                "⚠️ فقط کاربران عادی در صورت اسپم سکوت می‌شوند",
                parse_mode=ParseMode.HTML
            )
            logger.info(f"Spam mode disabled for admins in chat {chat.id} by user {user.id}")
    
    async def handle_group_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle messages in groups - delete non-admin messages and repost them"""
        chat = update.effective_chat
        user = update.effective_user
        message = update.message
        
        # Skip if it's not a group
        if chat.type not in ["group", "supergroup"]:
            return
        
        # Skip if user is admin
        if user.id in self.group_admins.get(chat.id, []):
            return
        
        # Skip if message is from bot itself
        if user.id == context.bot.id:
            return
        
        # Add to processing queue to prevent conflicts
        if chat.id not in self.processing_queues:
            self.processing_queues[chat.id] = asyncio.Queue()
            self.processing_locks[chat.id] = asyncio.Lock()
        
        # Add message to queue
        await self.processing_queues[chat.id].put((update, context))
        
        # Process queue if not already processing (with lock)
        if self.processing_queues[chat.id].qsize() == 1:
            # Use create_task for non-blocking execution
            asyncio.create_task(self._process_message_queue(chat.id))
    
    def _is_user_muted(self, chat_id: int, user_id: int) -> bool:
        """Check if user is currently muted"""
        mute_key = (chat_id, user_id)
        if mute_key in self.muted_users:
            mute_until = self.muted_users[mute_key]
            if datetime.now().timestamp() < mute_until:
                return True
            else:
                # Mute expired, remove from dict
                del self.muted_users[mute_key]
        return False
    
    def _check_spam(self, chat_id: int, user_id: int) -> bool:
        """Check if user is spamming and mute if necessary"""
        current_time = datetime.now().timestamp()
        message_key = (chat_id, user_id)
        
        # Initialize message times list if not exists
        if message_key not in self.user_message_times:
            self.user_message_times[message_key] = []
        
        # Add current message time
        self.user_message_times[message_key].append(current_time)
        
        # Keep only messages from last 60 seconds
        cutoff_time = current_time - 60
        self.user_message_times[message_key] = [
            msg_time for msg_time in self.user_message_times[message_key] 
            if msg_time > cutoff_time
        ]
        
        # Check if user sent more than 10 messages in last 60 seconds
        if len(self.user_message_times[message_key]) > 10:
            # Mute user for 30 minutes (1800 seconds)
            mute_until = current_time + 1800
            self.muted_users[(chat_id, user_id)] = mute_until
            
            # Clear message history
            self.user_message_times[message_key] = []
            
            logger.warning(f"User {user_id} muted for spam in chat {chat_id} until {datetime.fromtimestamp(mute_until)}")
            return True
        
        return False

    async def _process_message_queue(self, chat_id: int):
        """Process messages in queue one by one to prevent conflicts"""
        async with self.processing_locks[chat_id]:
            while not self.processing_queues[chat_id].empty():
                try:
                    update, context = await self.processing_queues[chat_id].get()
                    # Add small delay to ensure proper sequencing
                    await asyncio.sleep(0.05)
                    await self._process_single_message(update, context)
                    self.processing_queues[chat_id].task_done()
                except Exception as e:
                    logger.error(f"Error processing message in queue for chat {chat_id}: {e}")
                    # Mark task as done even if failed
                    try:
                        self.processing_queues[chat_id].task_done()
                    except ValueError:
                        pass
    
    async def _process_single_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process a single message with ultra-fast optimization"""
        chat = update.effective_chat
        user = update.effective_user
        message = update.message
        
        try:
            # Check if user is admin and spam mode is disabled for admins
            is_admin = user.id in self.group_admins.get(chat.id, [])
            spam_mode_for_admins = self.spam_mode_enabled.get(chat.id, False)
            
            if is_admin and not spam_mode_for_admins:
                # Admin users with spam mode disabled - skip spam detection
                pass
            else:
                # Non-admin users OR admins with spam mode enabled - check for spam
                # Check if user is muted
                if self._is_user_muted(chat.id, user.id):
                    await message.delete()
                    logger.info(f"Deleted message from muted user {user.id} in chat {chat.id}")
                    return
                
                # Check for spam
                if self._check_spam(chat.id, user.id):
                    await message.delete()
                    # Send mute notification
                    user_type = "ادمین" if is_admin else "کاربر"
                    await context.bot.send_message(
                        chat_id=chat.id,
                        text=f"⚠️ {user_type} <b>{user.first_name or 'کاربر'}</b> به دلیل اسپم به مدت 30 دقیقه سکوت شد!",
                        parse_mode=ParseMode.HTML
                    )
                    logger.info(f"User {user.id} ({'admin' if is_admin else 'user'}) muted for spam in chat {chat.id}")
                    return
            
            # Get user display name (only name, no ID) - with caching
            if user.id in self.user_name_cache:
                user_name = self.user_name_cache[user.id]
            else:
                user_name = user.first_name or "کاربر"
                if user.last_name:
                    user_name += f" {user.last_name}"
                # Cache the name for future use
                self.user_name_cache[user.id] = user_name
            
            # Fast message type detection
            message_type = "پیام"
            media_to_forward = None
            
            if message.text:
                message_type = "متن"
                # Get reply message ID if exists
                reply_to_message_id = message.reply_to_message.message_id if message.reply_to_message else None
                
                # Delete and send text simultaneously
                await asyncio.gather(
                    message.delete(),
                    context.bot.send_message(
                        chat_id=chat.id,
                        text=f"<b>{user_name}:</b>\n{message.text}",
                        parse_mode=ParseMode.HTML,
                        reply_to_message_id=reply_to_message_id
                    )
                )
            elif message.sticker:
                message_type = "استیکر"
                media_to_forward = message.sticker
            elif message.photo:
                message_type = "عکس"
                media_to_forward = message.photo[-1]
            elif message.video:
                message_type = "ویدیو"
                media_to_forward = message.video
            elif message.voice:
                message_type = "صدا"
                media_to_forward = message.voice
            elif message.video_note:
                message_type = "ویدیو نوت"
                media_to_forward = message.video_note
            elif message.document:
                message_type = "فایل"
                media_to_forward = message.document
            elif message.audio:
                message_type = "آهنگ"
                media_to_forward = message.audio
            elif message.animation:
                message_type = "گیف"
                media_to_forward = message.animation
            elif message.contact:
                message_type = "مخاطب"
                media_to_forward = message.contact
            elif message.location:
                message_type = "موقعیت"
                media_to_forward = message.location
            elif message.poll:
                message_type = "نظرسنجی"
                media_to_forward = message.poll
            else:
                message_type = "رسانه"
            
            # For media messages, process based on type
            if media_to_forward:
                # Get reply message ID if exists
                reply_to_message_id = message.reply_to_message.message_id if message.reply_to_message else None
                
                # First delete the original message
                await message.delete()
                
                # For stickers: send name + sticker separately (2 messages)
                if message.sticker:
                    # Send name message first
                    await context.bot.send_message(
                        chat_id=chat.id,
                        text=f"<b>{user_name}:</b>",
                        parse_mode=ParseMode.HTML,
                        reply_to_message_id=reply_to_message_id
                    )
                    # Then send sticker
                    await context.bot.send_sticker(
                        chat_id=chat.id,
                        sticker=media_to_forward,
                        reply_to_message_id=reply_to_message_id
                    )
                
                # For other media: send with caption in one message
                elif message.photo:
                    await context.bot.send_photo(
                        chat_id=chat.id,
                        photo=media_to_forward,
                        caption=f"<b>{user_name}:</b>",
                        parse_mode=ParseMode.HTML,
                        reply_to_message_id=reply_to_message_id
                    )
                elif message.video:
                    await context.bot.send_video(
                        chat_id=chat.id,
                        video=media_to_forward,
                        caption=f"<b>{user_name}:</b>",
                        parse_mode=ParseMode.HTML,
                        reply_to_message_id=reply_to_message_id
                    )
                elif message.voice:
                    await context.bot.send_voice(
                        chat_id=chat.id,
                        voice=media_to_forward,
                        caption=f"<b>{user_name}:</b>",
                        parse_mode=ParseMode.HTML,
                        reply_to_message_id=reply_to_message_id
                    )
                elif message.video_note:
                    # Video notes can't have captions, so use 2 messages
                    await context.bot.send_message(
                        chat_id=chat.id,
                        text=f"<b>{user_name}:</b>",
                        parse_mode=ParseMode.HTML,
                        reply_to_message_id=reply_to_message_id
                    )
                    await context.bot.send_video_note(
                        chat_id=chat.id,
                        video_note=media_to_forward,
                        reply_to_message_id=reply_to_message_id
                    )
                elif message.document:
                    await context.bot.send_document(
                        chat_id=chat.id,
                        document=media_to_forward,
                        caption=f"<b>{user_name}:</b>",
                        parse_mode=ParseMode.HTML,
                        reply_to_message_id=reply_to_message_id
                    )
                elif message.audio:
                    await context.bot.send_audio(
                        chat_id=chat.id,
                        audio=media_to_forward,
                        caption=f"<b>{user_name}:</b>",
                        parse_mode=ParseMode.HTML,
                        reply_to_message_id=reply_to_message_id
                    )
                elif message.animation:
                    await context.bot.send_animation(
                        chat_id=chat.id,
                        animation=media_to_forward,
                        caption=f"<b>{user_name}:</b>",
                        parse_mode=ParseMode.HTML,
                        reply_to_message_id=reply_to_message_id
                    )
                elif message.contact:
                    await context.bot.send_contact(
                        chat_id=chat.id,
                        contact=media_to_forward,
                        reply_to_message_id=reply_to_message_id
                    )
                elif message.location:
                    await context.bot.send_location(
                        chat_id=chat.id,
                        location=media_to_forward,
                        reply_to_message_id=reply_to_message_id
                    )
                elif message.poll:
                    await context.bot.send_poll(
                        chat_id=chat.id,
                        question=media_to_forward.question,
                        options=[option.text for option in media_to_forward.options],
                        is_anonymous=media_to_forward.is_anonymous,
                        reply_to_message_id=reply_to_message_id
                    )
            
            logger.info(f"Ultra-fast processed {message_type} from {user_name} in chat {chat.id}")
            
        except TelegramError as e:
            logger.error(f"Error handling message from user {user.id} in chat {chat.id}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error handling message: {e}")
    
    async def handle_new_chat_members(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle new chat members"""
        chat = update.effective_chat
        
        # Check if bot was added to the group
        new_members = update.message.new_chat_members
        for member in new_members:
            if member.id == context.bot.id:
                await update.message.reply_text(
                    "🤖 <b>ربات مدیریت گروه ادمین</b>\n\n"
                    "سلام! من برای مدیریت گروه‌هایی طراحی شده‌ام که فقط ادمین‌ها اجازه ارسال پیام دارند.\n\n"
                    "📋 <b>برای شروع:</b>\n"
                    "1. دسترسی ادمین به من بدهید\n"
                    "2. دستور /setup را اجرا کنید\n\n"
                    "برای راهنما: /help",
                    parse_mode=ParseMode.HTML
                )
                break
    
    async def handle_left_chat_member(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle left chat members"""
        chat = update.effective_chat
        left_member = update.message.left_chat_member
        
        # Check if bot was removed from the group
        if left_member.id == context.bot.id:
            # Clean up admin list for this chat
            if chat.id in self.group_admins:
                del self.group_admins[chat.id]
                logger.info(f"Cleaned up admin list for chat {chat.id} after bot removal")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Exception while handling an update: {context.error}")
        
        # Try to send error message to user if possible
        try:
            if update and update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="❌ خطایی رخ داد. لطفاً دوباره تلاش کنید."
                )
        except Exception as e:
            logger.error(f"Error sending error message: {e}")
    
    async def post_init(self, application: Application):
        """Post initialization - set bot commands"""
        commands = [
            BotCommand("start", "شروع ربات"),
            BotCommand("help", "راهنمای استفاده"),
            BotCommand("setup", "تنظیم ربات در گروه"),
            BotCommand("status", "وضعیت ربات و ادمین‌ها"),
            BotCommand("refresh_admins", "بروزرسانی لیست ادمین‌ها"),
            BotCommand("unmute", "حذف سکوت کاربر (ادمین)"),
            BotCommand("spam_mode", "فعال/غیرفعال کردن ضد اسپم برای ادمین‌ها"),
        ]
        
        await application.bot.set_my_commands(commands)
        logger.info("Bot commands set successfully")
    
    def run(self):
        """Run the bot"""
        logger.info("Starting Admin Group Bot...")
        
        # Add post_init callback
        self.application.post_init = self.post_init
        
        # Run the bot
        self.application.run_polling()

if __name__ == "__main__":
    bot = AdminGroupBot()
    bot.run()

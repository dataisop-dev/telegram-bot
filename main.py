import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Logging setup (Railway logs mein errors dekhne ke liye)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- AAPKI DETAILS ---
BOT_TOKEN = "8549491794:AAGNRdNevoiOOmJCGcFql5vHX2scXCccIME"
CHANNEL_ID = "@Nezukotest112"

async def check_membership(user_id, context):
    try:
        # Bot check karega ki user channel ka member hai ya nahi
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"Membership check error: {e}")
        return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Admin ya Bots ko mute nahi karna hai
    member_check = await update.effective_chat.get_member(user_id)
    if member_check.status in ['administrator', 'creator'] or update.effective_user.is_bot:
        return

    # Check membership
    is_member = await check_membership(user_id, context)

    if not is_member:
        try:
            # Message delete karein
            await update.message.delete()
            
            # User ko 1 min ke liye mute karein (Permissions restrict)
            mute_permissions = ChatPermissions(can_send_messages=False)
            await context.bot.restrict_chat_member(chat_id, user_id, permissions=mute_permissions)

            # Join button dikhayein
            keyboard = [
                [Inline

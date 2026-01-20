from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ChatMemberHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_USERNAME = "@YourPublicChannel"   # yaha apna public channel username daalna (example: @LTCNews)

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    try:
        # Check if user is channel member
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

        if member.status not in ["member", "administrator", "creator"]:
            # Not joined → Delete msg + mute
            await update.message.delete()

            await context.bot.restrict_chat_member(
                chat_id,
                user_id,
                ChatPermissions(can_send_messages=False),
                until_date=int(update.message.date.timestamp()) + 60,  # 60 sec mute
            )

            await update.message.reply_text(
                f"❌ Pehle {CHANNEL_USERNAME} join karo. Tab tak 1 minute mute ho."
            )

    except:
        pass


async def on_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.chat_member.new_chat_member.user.id
    chat_id = update.chat_member.chat.id

    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

        if member.status in ["member", "administrator", "creator"]:
            # User joined → unmute
            await context.bot.restrict_chat_member(
                chat_id,
                user_id,
                ChatPermissions(can_send_messages=True)
            )

            await context.bot.send_message(
                chat_id,
                f"✅ {update.chat_member.new_chat_member.user.full_name} ne channel join kar liya. Unmute kar diya!"
            )
    except:
        pass


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
app.add_handler(ChatMemberHandler(on_member_update, ChatMemberHandler.CHAT_MEMBER))

app.run_polling()
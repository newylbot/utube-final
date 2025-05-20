from pyrogram import filters
from pyrogram import enums
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)

from ..config import Config
from ..translations import Messages as tr  # Importing Messages class
from ..utubebot import UtubeBot
from ..youtube import GoogleAuth


# Function to close the help message
async def close_buttons(q: CallbackQuery):
    await q.message.delete()


@UtubeBot.on_message(
    filters.private
    & filters.incoming
    & filters.command(["help", "h"])
    & filters.user(Config.AUTH_USERS)
)
async def _help(c: UtubeBot, m: Message):
    await m.reply_chat_action(enums.ChatAction.TYPING)

    help_text = (
        f"📌 **How I Work:**\n"
        "1️⃣ **Authorize** me to upload to your YouTube channel. 📲\n"
        "2️⃣ **Forward** any Telegram video to me. 🎥\n"
        "3️⃣ **Reply** `/upload` or `/u` to upload. You can also add a title after the command.\n"
        "4️⃣ I **process & upload** the video to YouTube. 🚀\n"
        "5️⃣ You get the **YouTube link** after the upload. ✅\n"
        "6️⃣ Use `/createplaylist` or `/cp` to create a playlist. Choose the privacy, then type the name.\n\n"
        
        "🔔 **Notes:**\n"
    "🚫 **Daily Upload Limit:** YouTube API allows ~6 uploads per day due to quota limits.\n"
    "🛡️ **Unverified Apps:** Uploaded videos will stay private unless the app is verified by Google.\n"
    "⚠️ **Copyright:** Uploading copyrighted content may lead to video removal.\n\n"
        
        f"📺 **Create a YouTube Channel:**\n"
        "1️⃣ Sign in to YouTube on your phone or PC. 🖥️\n"
        "2️⃣ Try uploading a video or creating a playlist. 🎬\n"
        "3️⃣ If you don’t have a channel yet, follow the steps to create one. 🔥\n"
        "4️⃣ Confirm & start uploading! 🚀\n\n"
        
        f"✅ **Verify Your YouTube Account:**\n"
        "⚠️ Unverified accounts can only upload videos up to 15 minutes.\n"
        "[Verify your account here](http://www.youtube.com/verify) 🔗\n\n"
        
        f"🔑 **Authorize Me:**\n"
        "1️⃣ Click the provided link & allow access. 🔗\n"
        "2️⃣ Copy the given code. 📋\n"
        "3️⃣ Come back & send `/authorise copied-code` or `/a`.\n\n"
        "🔒 Your privacy is safe. I only help with uploads!\n\n"

        f"🔑 **To Logout & Re-Login Again:**\n"
        "1️⃣ Just do /lo or /logout to **Logout.....** \n"
        "2️⃣ Then Re-login by the the process..... \n"
        "3️⃣ Do /status or /st to check login Status.......\n"
        "4️⃣ Now You're Good to go.... \n\n"
        
        f"❌ To close this help message, press the 'Close' button below."
    )

    # Sign-in URL
    auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)
    auth_url = auth.GetAuthUrl()

    await m.reply_text(
        text=help_text,
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="🔑 Sign-In URL", url=auth_url),
                InlineKeyboardButton(text="❌ Close", callback_data="close_help")
            ]
        ]),
        disable_web_page_preview=True
    )


@UtubeBot.on_callback_query(filters.regex("^close_help$"))
async def close_help(c: UtubeBot, q: CallbackQuery):
    await close_buttons(q)

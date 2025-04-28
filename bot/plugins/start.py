from pyrogram import filters as Filters
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import os
import platform

from ..translations import Messages as tr
from ..config import Config
from ..utubebot import UtubeBot


@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("start")
    & Filters.user(Config.AUTH_USERS)
)
async def _start(c: UtubeBot, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)

    await m.reply_text(
        text=tr.START_MSG.format(m.from_user.first_name),
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Updated the code by ๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ", url="https://t.me/itz_lumino")]]
        ),
    )


@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command(["status", "st"])
    & Filters.user(Config.AUTH_USERS)
)
async def _status(c: UtubeBot, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)

    auth_status = "✅ Logged In" if os.path.exists("auth_token.txt") else "❌ Not Logged In"

    text = f"""
<b>🤖 Bot Status:</b>

<b>Authentication:</b> {auth_status}
<b>Allowed Users:</b> {len(Config.AUTH_USERS)}
<b>Bot Version:</b>  ʀᴇx - ᴅ  <b>v28.04.2025</b>
<b>Python Version:</b> {platform.python_version()}
<b>Server:</b> {'Heroku' if os.getenv('DYNO') else '๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ'}

"""
    await m.reply_text(
        text=text,
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("๏ Support ⇗", url="https://t.me/itz_lumino")]]
        ),
    )

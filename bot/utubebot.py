import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
)
from .config import Config
from bot.database import Database  # Import the new SQLite-based Database class
from bot.youtube import GoogleAuth, YouTube
from bot.translations import Messages as tr

class UtubeBot(Client):
    def __init__(self):
        super().__init__(
            Config.SESSION_NAME,
            bot_token=Config.BOT_TOKEN,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            plugins=dict(root="bot.plugins"),
            workers=6,
        )
        self.DOWNLOAD_WORKERS = 6
        self.counter = 0
        self.download_controller = {}
        self.playlist_create = {}
        self.db = Database()  # Initialize SQLite database connection
        self.add_dynamic_commands()  # Register commands

    def add_dynamic_commands(self):
        # Set Prefix Command
        @self.on_message(filters.command(["setprefix", "setp"]) & filters.user(Config.BOT_OWNER))
        async def set_prefix(client, message):
            if len(message.command) < 2:
                await message.reply(
                    "Usage: `/setprefix Your Prefix Text` or `/setp Your Prefix Text`",
                    quote=True
                )
                return
            prefix = message.text.split(" ", 1)[1]
            self.db.update_setting("video_title_prefix", prefix)  # Update with SQLite
            await message.reply(f"✅ Prefix updated to:\n`{prefix}`", quote=True)

        # Set Suffix Command
        @self.on_message(filters.command(["setsuffix", "sets"]) & filters.user(Config.BOT_OWNER))
        async def set_suffix(client, message):
            if len(message.command) < 2:
                await message.reply(
                    "Usage: `/setsuffix Your Suffix Text` or `/sets Your Suffix Text`",
                    quote=True
                )
                return
            suffix = message.text.split(" ", 1)[1]
            self.db.update_setting("video_title_suffix", suffix)  # Update with SQLite
            await message.reply(f"✅ Suffix updated to:\n`{suffix}`", quote=True)

        # Set Playlist ID Command
        @self.on_message(filters.command(["setplaylist", "setpid"]) & filters.user(Config.BOT_OWNER))
        async def set_playlist(client, message):
            if len(message.command) < 2:
                await message.reply(
                    "Usage: `/setplaylist PlaylistID` or `/setpid PlaylistID`",
                    quote=True
                )
                return
            playlist_id = message.text.split(" ", 1)[1]
            self.db.update_setting("playlist_id", playlist_id)  # Update with SQLite
            await message.reply(f"✅ Playlist ID updated to:\n`{playlist_id}`", quote=True)

        # Create Playlist Command (interactive)
        @self.on_message(filters.command(["createplaylist", "cp"]) & filters.user(Config.BOT_OWNER))
        async def create_playlist_cmd(client, message: Message):
            if not os.path.exists(Config.CRED_FILE):
                await message.reply(tr.NOT_AUTHENTICATED_MSG, quote=True)
                return

            self.playlist_create[message.from_user.id] = {"stage": "privacy"}
            keyboard = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Private", callback_data="pl_priv_private"),
                    InlineKeyboardButton("Unlisted", callback_data="pl_priv_unlisted"),
                    InlineKeyboardButton("Public", callback_data="pl_priv_public"),
                ]]
            )
            await message.reply(
                "Choose playlist privacy:",
                quote=True,
                reply_markup=keyboard,
            )

        @self.on_callback_query(filters.regex("^pl_priv_") & filters.user(Config.BOT_OWNER))
        async def playlist_privacy_cb(client, query: CallbackQuery):
            user_id = query.from_user.id
            if user_id not in self.playlist_create:
                await query.answer("Use /cp first", show_alert=True)
                return
            privacy = query.data.split("_")[-1]
            self.playlist_create[user_id] = {"stage": "title", "privacy": privacy}
            await query.message.edit_text("Send me the playlist name:")

        @self.on_message(filters.text & filters.user(Config.BOT_OWNER))
        async def playlist_name_step(client, message: Message):
            state = self.playlist_create.get(message.from_user.id)
            if not state or state.get("stage") != "title" or message.text.startswith("/"):
                return

            title = message.text
            privacy = state.get("privacy", "private")
            loop = asyncio.get_running_loop()
            try:
                auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)
                auth.LoadCredentialsFile(Config.CRED_FILE)
                google = await loop.run_in_executor(None, auth.authorize)
                youtube = YouTube(google)
                playlist_id = await loop.run_in_executor(
                    None,
                    youtube.create_playlist,
                    title,
                    "",
                    privacy,
                )
                self.db.update_setting("playlist_id", playlist_id)
                await message.reply(
                    f"✅ Playlist `{title}` created with ID `{playlist_id}` and set as default.",
                    quote=True,
                )
            except Exception as e:
                await message.reply(f"❌ Failed to create playlist: {e}", quote=True)
            finally:
                self.playlist_create.pop(message.from_user.id, None)

        # Show Current Settings Command
        @self.on_message(filters.command(["showsettings", "shows"]) & filters.user(Config.BOT_OWNER))
        async def show_settings(client, message):
            settings = self.db.get_settings()  # Get settings from SQLite
            reply = (
                "**Current Settings:**\n\n"
                f"**Prefix:** `{settings.get('video_title_prefix', '')}`\n"
                f"**Suffix:** `{settings.get('video_title_suffix', '')}`\n"
                f"**Playlist ID:** `{settings.get('playlist_id', '')}`"
            )
            await message.reply(reply, quote=True)

        # Reshow Command (clear all settings)
        @self.on_message(filters.command(["resetshows", "reshows"]) & filters.user(Config.BOT_OWNER))
        async def reshow(client, message):
            # Clear stored prefix, suffix, and playlist ID
            self.db.update_setting("video_title_prefix", "")
            self.db.update_setting("video_title_suffix", "")  # You can remove this if you don't want to change the Suffix 
            self.db.update_setting("playlist_id", "")
            await message.reply(
                "✅ All settings have been cleared (prefix, suffix, playlist ID).",
                quote=True
            )

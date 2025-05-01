from pyrogram import Client, filters
from .config import Config
from bot.database import Database

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
        self.db = Database()  # Initialize MongoDB connection
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
            self.db.update_setting("video_title_prefix", prefix)
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
            self.db.update_setting("video_title_suffix", suffix)
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
            self.db.update_setting("playlist_id", playlist_id)
            await message.reply(f"✅ Playlist ID updated to:\n`{playlist_id}`", quote=True)

        # Show Current Settings Command
        @self.on_message(filters.command(["showsettings", "shows"]) & filters.user(Config.BOT_OWNER))
        async def show_settings(client, message):
            settings = self.db.get_settings()
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
            self.db.update_setting("video_title_suffix", "")
            self.db.update_setting("playlist_id", "")
            await message.reply(
                "✅ All settings have been cleared (prefix, suffix, playlist ID).",
                quote=True
            )

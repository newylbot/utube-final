import os
import random
import asyncio
import logging
from typing import Optional, Tuple

from ..youtube import GoogleAuth, YouTube
from ..config import Config
from ..helpers.watermark import Watermark  # ✅ Correct Import

log = logging.getLogger(__name__)

class Uploader:
    def __init__(self, file: str, title: Optional[str] = None, thumbnail: Optional[str] = None):
        self.file = file
        self.title = title
        self.thumbnail = thumbnail  # Store thumbnail path
        self.watermarked_file = None  # Store path of watermarked video
        self.video_category = {
            1: "Film & Animation",
            2: "Autos & Vehicles",
            10: "Music",
            15: "Pets & Animals",
            17: "Sports",
            19: "Travel & Events",
            20: "Gaming",
            22: "People & Blogs",
            23: "Comedy",
            24: "Entertainment",
            25: "News & Politics",
            26: "Howto & Style",
            27: "Education",
            28: "Science & Technology",
            29: "Nonprofits & Activism",
        }

    async def start(self, progress: callable = None, *args) -> Tuple[bool, str]:
        self.progress = progress
        self.args = args

        await self._upload()

        return self.status, self.message

    async def _upload(self) -> None:
        try:
            loop = asyncio.get_running_loop()

            auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)

            if not os.path.isfile(Config.CRED_FILE):
                log.debug(f"{Config.CRED_FILE} does not exist")
                self.status = False
                self.message = "Upload failed because you did not authenticate me."
                return

            auth.LoadCredentialsFile(Config.CRED_FILE)
            google = await loop.run_in_executor(None, auth.authorize)

            # Select category
            categoryId = Config.VIDEO_CATEGORY if Config.VIDEO_CATEGORY in self.video_category else random.choice(list(self.video_category))
            categoryName = self.video_category[categoryId]

            # Set title
            title = self.title if self.title else os.path.basename(self.file)
            title = (
                (Config.VIDEO_TITLE_PREFIX + "🔥 " + title + " 🚀" + Config.VIDEO_TITLE_SUFFIX)
                .replace("<", "")
                .replace(">", "")[:100]
            )

            # Set description
            description = (
                Config.VIDEO_DESCRIPTION
                + "\n\n📢 *Uploaded to YouTube* 🎥"
                + "\n🚀 *By:* ๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ (@itz_lumino)"
                + "\n\n💬 *Join Us on Telegram:*"
                + "\n👉 *@luminoxpp*"
                + "\n\n🔥 *Get Exciting Batches at Very Low Cost!* 💰"
            )[:5000]

            # Set privacy status
            privacyStatus = Config.UPLOAD_MODE if Config.UPLOAD_MODE else "private"

            properties = dict(
                title=title,
                description=description,
                category=categoryId,
                privacyStatus=privacyStatus,
            )

            log.debug(f"Payload for {self.file} : {properties}")

            # 🔹 **Apply watermark if enabled**
            if Config.WATERMARK_ENABLED:
                log.debug("Applying watermark to the video...")
                wm = Watermark(self.file, Config.WATERMARK_IMAGE)
                self.watermarked_file = await loop.run_in_executor(None, wm.apply)
                if self.watermarked_file and self.watermarked_file != self.file:
                    log.debug(f"Watermark applied: {self.watermarked_file}")
                else:
                    log.error("Failed to apply watermark. Proceeding with original video.")
                    self.watermarked_file = self.file
            else:
                self.watermarked_file = self.file

            youtube = YouTube(google)
            r = await loop.run_in_executor(None, youtube.upload_video, self.watermarked_file, properties)

            video_id = r["id"]

            # Upload thumbnail if provided
            if self.thumbnail and os.path.exists(self.thumbnail):
                await loop.run_in_executor(None, youtube.upload_thumbnail, video_id, self.thumbnail)
                log.debug(f"Thumbnail uploaded: {self.thumbnail}")

            self.status = True
            self.message = (
                f"[{title}](https://youtu.be/{video_id}) uploaded to YouTube under category "
                f"{categoryId} ({categoryName})"
            )

            # ✅ Delete the processed file after upload
            if os.path.exists(self.watermarked_file) and self.watermarked_file != self.file:
                os.remove(self.watermarked_file)
                log.debug(f"Deleted watermarked file: {self.watermarked_file}")

            if os.path.exists(self.file):
                os.remove(self.file)
                log.debug(f"Deleted original file: {self.file}")

        except Exception as e:
            log.error(e, exc_info=True)
            self.status = False
            self.message = f"Error occurred during upload.\nError details: {e}"

import os
import time
import string
import random
import logging
import asyncio
import datetime
from typing import Tuple, Union

from pyrogram import StopTransmission
from pyrogram import filters as Filters
from pyrogram import enums  # Add this at the top if not already present
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from ..translations import Messages as tr
from ..helpers.downloader import Downloader
from ..helpers.uploader import Uploader
from ..config import Config
from ..utubebot import UtubeBot


log = logging.getLogger(__name__)


@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command(["upload", "u"])
    & Filters.user(Config.AUTH_USERS)
)
async def _upload(c: UtubeBot, m: Message):
    if not os.path.exists(Config.CRED_FILE):
        await m.reply_text(tr.NOT_AUTHENTICATED_MSG, True)
        return

    if not m.reply_to_message:
        await m.reply_text(tr.NOT_A_REPLY_MSG, True)
        return

    message = m.reply_to_message

    if not message.media or not valid_media(message):
        await m.reply_text(tr.NOT_A_MEDIA_MSG, True)
        return

    # ✅ Remove daily quota check for unlimited uploads
    # if c.counter >= 6:
    #     await m.reply_text(tr.DAILY_QOUTA_REACHED, True)
    #     return

    snt = await m.reply_text(tr.PROCESSING, True)

    download_id = get_download_id(c.download_controller)
    c.download_controller[download_id] = True

    download = Downloader(m)
    status, file = await download.start(progress, snt, c, download_id)
    log.debug(f"{status}: {file}")
    c.download_controller.pop(download_id)

    if not status:
        await snt.edit_text(text=file, parse_mode="markdown")
        return

    try:
        await snt.edit_text("✅ Downloaded! Now uploading to YouTube...")
    except Exception as e:
        log.warning(e, exc_info=True)

    title = " ".join(m.command[1:])
    upload = Uploader(file, title)
    status, link = await upload.start(progress, snt)
    log.debug(f"{status}: {link}")

    await snt.edit_text(text=link, parse_mode=enums.ParseMode.MARKDOWN)


def get_download_id(storage: dict) -> str:
    while True:
        download_id = "".join([random.choice(string.ascii_letters) for _ in range(3)])
        if download_id not in storage:
            break
    return download_id


def valid_media(media: Message) -> bool:
    if media.video:
        return True
    elif media.video_note:
        return True
    elif media.animation:
        return True
    elif media.document and "video" in media.document.mime_type:
        return True
    else:
        return False


def human_bytes(
    num: Union[int, float], split: bool = False
) -> Union[str, Tuple[int, str]]:
    base = 1024.0
    suffix_list = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    for unit in suffix_list:
        if abs(num) < base:
            if split:
                return round(num, 2), unit
            return f"{round(num, 2)} {unit}"
        num /= base


async def progress(
    cur: Union[int, float],
    tot: Union[int, float],
    start_time: float,
    status: str,
    snt: Message,
    c: UtubeBot,
    download_id: str,
):
    if not c.download_controller.get(download_id):
        raise StopTransmission

    try:
        diff = int(time.time() - start_time)

        if (int(time.time()) % 5 == 0) or (cur == tot):
            await asyncio.sleep(1)
            speed, unit = human_bytes(cur / diff, True)
            curr = human_bytes(cur)
            tott = human_bytes(tot)
            eta = datetime.timedelta(seconds=int(((tot - cur) / (1024 * 1024)) / speed))
            elapsed = datetime.timedelta(seconds=diff)
            progress = round((cur * 100) / tot, 2)
            text = f"{status}\n\n{progress}% done.\n{curr} of {tott}\nSpeed: {speed} {unit}PS"
            f"\nETA: {eta}\nElapsed: {elapsed}"
            await snt.edit_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Cancel!", f"cncl+{download_id}")]]
                ),
            )

    except Exception as e:
        log.info(e)
        pass

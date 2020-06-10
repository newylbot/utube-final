from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton

from ..translations import Messages as tr
from ..config import Config
from ..utubebot import UtubeBot


@UtubeBot.on_message(
    Filters.private 
    & Filters.incoming
    & Filters.command('start')
    & Filters.user()
)
async def _start(c, m):
    await m.reply_chat_action("typing")
    
    await m.reply_text(
        text=tr.START_MSG.format(m.from_user.first_name),
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Join Project Channel!', url='https://t.me/odbots')
                ]
            ]
        )
    )

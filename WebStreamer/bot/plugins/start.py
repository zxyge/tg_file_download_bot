# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]
import logging

from pyrogram import filters
from pyrogram.types import Message
from WebStreamer.bot import StreamBot


@StreamBot.on_message(filters.command(["start", "help"]))
async def start(_, m: Message):
    try:
        await m.reply(
            f'Hi {m.from_user.mention(style="md")}, Send me a file to get an instant stream link.'
        )
    except Exception as e:
        logging.info(f'Replay start message error: {e}')

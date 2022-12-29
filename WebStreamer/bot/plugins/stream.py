# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import logging
from pyrogram import filters
from WebStreamer.vars import Var
from urllib.parse import quote_plus
from WebStreamer.bot import StreamBot
from WebStreamer.utils import get_hash, get_name, get_file_size, get_media_type, get_unique_id
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from WebStreamer.utils.media_download import queue




@StreamBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ),
    group=4,
)


async def media_receive_handler(_, m: Message):
    log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
    file_hash = get_hash(log_msg, Var.HASH_LENGTH)
    file_name = get_name(m)
    file_size = get_file_size(m)
    stream_link = f"{Var.URL}{log_msg.id}/{quote_plus(file_name)}?hash={file_hash}"
    short_link = f"{Var.URL}{file_hash}{log_msg.id}"
    url = "http://127.0.0.1:{}/{}/{}?hash={}".format(Var.PORT, log_msg.id, quote_plus(file_name), file_hash)
    if file_name == '':
        file_type = get_media_type(m)
        file_name = f'{get_unique_id(m)}.{file_type}'
    for filter in Var.FILTER_WORDS:
        if filter in file_name:
            file_name = file_name.replace(filter, '')
    rm = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Open", url=stream_link)]]
    )
    if Var.FQDN == Var.BIND_ADDRESS:
        # dkabl
        rm = None
    await m.reply_text(
        text="'{}' \n\nPut into download queue\n\nLink: <a href='{}'>{}</a>".format(file_name, short_link, short_link),
        quote=True,
        parse_mode=ParseMode.HTML,
        reply_markup=rm,
    )
    queue.put({
        'url': url,
        'file_name': file_name,
        'file_size': file_size,
        'm': m.from_user.id
    })
    logging.info(f"{file_name} Put into download queue")
    # logging.info(f"link: {url}")
    # download(url, file_name, file_size, m.from_user.id)

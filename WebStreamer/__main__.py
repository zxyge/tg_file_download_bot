# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import sys
import asyncio
import logging
from .vars import Var
from aiohttp import web
from pyrogram import idle
from WebStreamer import utils
from WebStreamer import StreamBot
from WebStreamer.server import web_server
from WebStreamer.bot.clients import initialize_clients
# from WebStreamer.utils.media_download import start
# from WebStreamer


logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="[%(asctime)s][%(levelname)s] => %(message)s",
    handlers=[logging.StreamHandler(stream=sys.stdout),
              logging.FileHandler("streambot.log", mode="a", encoding="utf-8")],)

logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

server = web.AppRunner(web_server())

# if sys.version_info[1] > 9:
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
# else:
loop = asyncio.get_event_loop()

async def start_services():
    await StreamBot.start()
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    print(f"Staning - {StreamBot.username}")
    await initialize_clients()
    if Var.ON_HEROKU:
        print('Starting - Keep Alive Service')
        asyncio.create_task(utils.ping_server())
    print(f"Staning - Streamer Server")
    await server.setup()
    bind_address = "0.0.0.0" if Var.ON_HEROKU else Var.BIND_ADDRESS
    await web.TCPSite(server, bind_address, Var.PORT).start()
    print("------------------------- Service Info -------------------------")
    print("bot =>> {}".format(bot_info.first_name))
    if bot_info.dc_id:
        print("DC ID =>> {}".format(str(bot_info.dc_id)))
    print("server ip =>> {}".format(bind_address, Var.PORT))
    if Var.ON_HEROKU:
        print("app running on =>> {}".format(Var.FQDN))
    print("Keep running, use ctrl+c to stop service")
    print("---------------------------- DONE ------------------------------")
    await idle()


async def cleanup():
    await server.cleanup()
    await StreamBot.stop()


if __name__ == "__main__":
    try:
        print("-------------------------- StartIng --------------------------")
        utils.start()
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.error(err.with_traceback(None))
    finally:
        loop.run_until_complete(cleanup())
        loop.stop()
        print("------------------------ Stopped Services ------------------------")
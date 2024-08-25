import asyncio
import importlib
from pyrogram import idle
from Avoids import app, LOGGER
from Avoids.modules import ALL_MODULES


async def avoids():
    for all_module in ALL_MODULES:
        importlib.import_module(f"Avoids.modules.{all_module}")
    LOGGER.info(f"Successfully loaded {len(ALL_MODULES)}.")
    LOGGER.info("Bot Started")
    await idle()

    try:
        await app.stop()
    except:
        pass
    LOGGER.info("Stopping! GoodBye")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(avoids())

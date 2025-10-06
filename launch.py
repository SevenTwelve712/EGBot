import asyncio
import logging
from logging.handlers import RotatingFileHandler

from bot import run_bot
from conf import Conf


async def flush_handler(handler):
    while True:
        logging.info("handler flushed")
        handler.flush()
        await asyncio.sleep(120)

async def launch_bot_and_logs_saving():
    await asyncio.gather(run_bot(), flush_handler(rotating_file_handler))


if __name__ == "__main__":
    rotating_file_handler = RotatingFileHandler(f"{Conf.project_path}/logs/log.log", maxBytes=5000000, backupCount=5)
    logging.basicConfig(handlers=[rotating_file_handler], level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    asyncio.run(launch_bot_and_logs_saving())


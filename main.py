import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import settings
from discord_client import DiscordBridgeBot
from telegram_handlers import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    discord_bot = DiscordBridgeBot(channel_id=settings.dc_channel_id)

    tg_bot = Bot(token=settings.tg_token)
    dp = Dispatcher()

    dp.include_router(router)

    dp["discord_bot"] = discord_bot

    await asyncio.gather(
        dp.start_polling(tg_bot),
        discord_bot.start(settings.dc_token)
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Работа ботов завершена")
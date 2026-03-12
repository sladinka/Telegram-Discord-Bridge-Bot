import logging

import disnake
from disnake.ext import commands

logger = logging.getLogger(__name__)


class DiscordBridgeBot(commands.Bot):
    def __init__(self, channel_id: int):
        intents = disnake.Intents.default()
        super().__init__(command_prefix="+", intents=intents)
        self.target_channel_id = channel_id

    async def on_ready(self) -> None:
        logger.info("Discord bot запущен %s", self.user)

    async def send_forwarded_message(self, content: str, files: list[disnake.File]) -> None:
        channel = self.get_channel(self.target_channel_id)
        if not channel:
            try:
                channel = await self.fetch_channel(self.target_channel_id)
            except disnake.NotFound:
                logger.error("Discord канал %s не найден.", self.target_channel_id)
                return

        if not isinstance(channel, disnake.TextChannel):
            logger.error("Discord канал не является текстовым")
            return

        if len(content) > 2000:
            content = content[:1997] + "..."

        try:
            if content or files:
                await channel.send(content=content, files=files)
        except Exception as e:
            logger.exception("Ошибка отправки сообщения в Discord: %s", e)
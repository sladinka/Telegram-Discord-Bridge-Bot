import logging
from io import BytesIO
from typing import Optional

import disnake
from aiogram import Bot, F, Router
from aiogram.types import Message

from config import settings
from discord_client import DiscordBridgeBot
from formatter import format_to_discord_markdown

logger = logging.getLogger(__name__)
router = Router()


async def download_tg_file(bot: Bot, file_id: str, file_name: str) -> Optional[disnake.File]:
    try:
        file_info = await bot.get_file(file_id)
        file_bytes: Optional[BytesIO] = await bot.download_file(file_info.file_path)
        
        if not file_bytes:
            return None
            
        file_bytes.seek(0)
        return disnake.File(fp=file_bytes, filename=file_name)
    except Exception as e:
        logger.exception("Ошибка при скачивании файла %s: %s", file_id, e)
        return None


@router.channel_post(F.chat.id == settings.tg_channel_id)
async def forward_to_discord(message: Message, bot: Bot, discord_bot: DiscordBridgeBot) -> None:
    raw_text = message.text or message.caption or ""
    entities = message.entities or message.caption_entities

    formatted_text = format_to_discord_markdown(raw_text, entities)
    
    files: list[disnake.File] = []

    if message.photo:
        photo = message.photo[-1]  
        file = await download_tg_file(bot, photo.file_id, "photo.jpg")
        if file:
            files.append(file)
            
    elif message.video:
        video_name = message.video.file_name or "video.mp4"
        file = await download_tg_file(bot, message.video.file_id, video_name)
        if file:
            files.append(file)
            
    elif message.document:
        doc_name = message.document.file_name or "document.file"
        file = await download_tg_file(bot, message.document.file_id, doc_name)
        if file:
            files.append(file)

    if formatted_text or files:
        await discord_bot.send_forwarded_message(content=formatted_text, files=files)
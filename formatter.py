from aiogram.types import MessageEntity


def format_to_discord_markdown(text: str, entities: list[MessageEntity] | None) -> str:
    if not entities or not text:
        return text or ""

    encoded_text = text.encode("utf-16-le")

    sorted_entities = sorted(entities, key=lambda e: e.offset, reverse=True)
    
    for entity in sorted_entities:
        start = entity.offset * 2
        end = start + (entity.length * 2)
        
        content = encoded_text[start:end].decode("utf-16-le")

        if entity.type == "bold":
            replacement = f"**{content}**"
        elif entity.type == "italic":
            replacement = f"*{content}*"
        elif entity.type == "strikethrough":
            replacement = f"~~{content}~~"
        elif entity.type == "underline":
            replacement = f"__{content}__"
        elif entity.type == "code":
            replacement = f"`{content}`"
        elif entity.type == "pre":
            language = entity.language or ""
            replacement = f"```{language}\n{content}\n```"
        elif entity.type == "text_link":
            replacement = f"[{content}]({entity.url})"
        elif entity.type == "spoiler":
            replacement = f"||{content}||"
        else:
            replacement = content
            
        encoded_text = encoded_text[:start] + replacement.encode("utf-16-le") + encoded_text[end:]
        
    return encoded_text.decode("utf-16-le")
from aiogram.types import Message

MAX_LENGTH = 4096

async def safe_send_text(send, text: str, **kwargs):
    """
    Безопасная отправка длинного текста по кускам до 4096 символов.
    """

    chunks = [text[i:i+MAX_LENGTH] for i in range(0, len(text), MAX_LENGTH)]
    for chunk in chunks:
        await send(chunk, **kwargs)


async def safe_send_ration_for_week_response(send, text: str, **kwargs):

    data = text.split("===")
    days = data[0]
    helping = data[1]
    for day in days:
        if day.strip():  # Check if day is not empty
            chunks = [day[i:i+MAX_LENGTH] for i in range(0, len(day), MAX_LENGTH)]
            for chunk in chunks:
                await send(chunk, **kwargs)
    await send(helping, **kwargs)
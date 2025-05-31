from aiogram.dispatcher.middlewares.base import BaseMiddleware
from typing import Callable, Dict, Any
from aiogram.types import TelegramObject
from Classes.UserProfile import UserProfile
from db.services import load_user_profile
from db.session import async_session

class ProfileMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # Загружаем профиль только если хендлер его требует
        if "profile" in handler.__code__.co_varnames:
            user_id = event.from_user.id

            async with async_session() as session:
                data["profile"] = await load_user_profile(user_id, session)

        return await handler(event, data)
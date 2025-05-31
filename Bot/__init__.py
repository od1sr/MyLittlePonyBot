from aiogram import Bot, Dispatcher
from Config.bot import BOT_TOKEN
from .routers.user import user_router
from .middlewares.user import ProfileMiddleware
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(user_router)
dp.message.middleware(ProfileMiddleware())
dp.callback_query.middleware(ProfileMiddleware())

__all__ = ["bot", "dp"]
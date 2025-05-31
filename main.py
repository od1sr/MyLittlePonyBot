
from Bot import bot, dp
import asyncio
from db.session import init_db
from src.ai_base.utils import init_db as init_chroma_db

async def main():
    await init_db()
    chroma_client = init_chroma_db()

    dp['chroma_client'] = chroma_client
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

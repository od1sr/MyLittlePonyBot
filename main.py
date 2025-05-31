
from Bot import bot, dp
import asyncio
from db.session import init_db

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

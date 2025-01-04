from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging

import config as Config
from utils.notify_admin import on_startup, on_shutdown
from utils.bot_commands import set_default_commands
from app.middlewares import ThrottlingMiddleware
from app.handlers import routers  # Import all routers

async def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    storage = MemoryStorage()
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher(storage=storage)

    await on_startup(bot)
    await set_default_commands(bot)

    # Register all routers
    for router in routers:
        dp.include_router(router)

    dp.message.outer_middleware(ThrottlingMiddleware(limit=2, interval=1))
    await dp.start_polling(bot)
    await on_shutdown(bot)

if __name__ == "__main__":
    asyncio.run(main())

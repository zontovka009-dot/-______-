import asyncio
from aiogram import Bot,Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import config
from database.db import init_db
from handlers.start import router as start_router
from handlers.profile import router as profile_router
from handlers.games import router as games_router
from handlers.group import router as group_router
from handlers.admin import router as admin_router
from handlers.commands import router as commands_router

async def main():
    await init_db()
    bot=Bot(
        config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp=Dispatcher()
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(games_router)
    dp.include_router(admin_router)
    dp.include_router(commands_router)
    dp.include_router(group_router)

    print("🌙 The Endy • Genshin запущен.")
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())

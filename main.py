import asyncio
import os

from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
from database.zapusk import create_database, drop_database, session_maker
from handlers.private import private_router
from general.commands_list import commands_lst
from handlers.group import group_router
from aiogram.enums import ParseMode
from handlers.admin import admin_router
from middelwares.database import DataBaseSession


ALLOWED_UPDATES = ['message, edited_message']
bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
bot.my_admins_list = []
dp = Dispatcher()

dp.include_routers(private_router, group_router, admin_router)

async def on_startup(bot):
    params_run = False
    if params_run:
        await drop_database()
    await create_database()

async def on_shutdown(bot):
    print('Бот упал')

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.set_my_commands(commands=commands_lst, scope=types.BotCommandScopeAllPrivateChats())
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())

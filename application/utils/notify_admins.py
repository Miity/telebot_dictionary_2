import logging
from aiogram import Dispatcher
from application.loader import bot
from application.config import admins_id

logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)


async def on_start_notify(dp:Dispatcher):
    for admin in admins_id:
        try:
            await dp.bot.send_message(chat_id=admin, text='бот запущен.\n/start')
        except Exception as e:
            print('error in "on_start_notify" \n', e)
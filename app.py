async def on_startup(dp):

    from utils.notify_admins import on_start_notify
    await on_start_notify(dp)

    from utils.set_bot_commands import set_def_commands
    await set_def_commands(dp)


if __name__=='__main__':
    from aiogram import executor
    from handlers import dp

    
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
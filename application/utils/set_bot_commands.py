from aiogram import types


async def set_def_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'start or reset program'),
        types.BotCommand('cancel', 'cancel all'),
        types.BotCommand('menu', 'open menu')

    ])
from multiprocessing.connection import wait
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from application.loader import dp, bot
from googletrans import Translator

from application.keyboards.inline.keyboards import keyboard
from application.states.states import In_dictionary
from application_data.database.commands import add_word_to_dict, find_dict


@dp.message_handler(state=In_dictionary.start)
async def translate(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(str(data))

    tr = Translator()
    translate = tr.translate(message.text, data['dictionary']['language_dist'], src = data['dictionary']['language_src']).text
    await state.update_data(new_word = message.text)
    await state.update_data(translate = translate)

    await message.answer(text = '{} --> {}'.format(message.text, translate), reply_markup=keyboard)
    await bot.delete_message(message.from_user.id, message.message_id)


@dp.callback_query_handler(text='add_word', state=In_dictionary.start)
async def add_to_dict(callback: types.CallbackQuery, state:FSMContext):

    data = await state.get_data()
    print(str(data))

    new_word = callback.message.text.split('-->')[0]
    translate = callback.message.text.split('-->')[1]

    add_word_to_dict(data['dictionary']['id'], new_word, translate=translate)
    await callback.message.reply('{} - добавленно до вашого словнику.'.format(new_word))
    await callback.message.delete()
    
    await state.update_data(dictionary = find_dict(data['dictionary']['id']).get_as_dict())
    


@dp.callback_query_handler(text='edit_translate', state=In_dictionary.start)
async def edit_translate(callback: types.CallbackQuery, state:FSMContext):
    await callback.message.edit_reply_markup(None)
    await callback.message.reply('Введіть правельний переклад')
    await In_dictionary.edit_translate.set()

    text = callback.message.text
    new_word = text.split('-->')[0]

    await state.update_data(new_word = new_word)

@dp.message_handler(state=In_dictionary.edit_translate)
async def change_translate(message: types.Message, state:FSMContext):
    data = await state.get_data()
    await message.answer('{} --> {}'.format(data['new_word'], message.text), reply_markup=keyboard)
    await message.delete()
    await In_dictionary.start.set()


@dp.message_handler()
async def tarnslate(message: types.Message):
    tr = Translator()
    await message.answer(text = '{} --> {}'.format(message.text,tr.translate(message.text).text))
    await bot.delete_message(message.from_user.id, message.message_id)

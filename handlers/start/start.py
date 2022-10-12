import json
from copy import deepcopy
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text
from loader import dp

from keyboards.inline.keyboards import start_ikb, dict_contr_ikb
from data.database.commands import show_dicts, find_dict
from data.database.commands import find_or_new_user
from states.states import In_dictionary


@dp.message_handler(commands='cancel', state="*")
@dp.message_handler(commands='start', state=In_dictionary.start)
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message:types.Message, state: FSMContext = None):
    if state:
        await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Почнемо з початку')
    await start_bot(message)


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    print('bot started by user')
    user, found = find_or_new_user(message.from_id)
    if found:
        start_ikb_dicts = deepcopy(start_ikb)
        # перевірити чи є словарики
        dicts = show_dicts(user)
        # створити клавіатуру з назвами словариків
        for dictionary in dicts:
            print('open_dict_{}'.format(str(dictionary.id)))
            start_ikb_dicts.add(types.InlineKeyboardButton(dictionary.title, 
                                callback_data='open_dict_{}'.format(str(dictionary.id))))
        await message.answer('Привіт')
        await message.answer('Відкриємо словарик, чи створемо новий?', reply_markup=start_ikb_dicts)
    else:
        await message.answer('Привіт новенький.')
        await message.answer('В тебе ще нема словників, тож давай створемо новий.', reply_markup=start_ikb)


@dp.callback_query_handler(lambda callback: callback.data.split('_')[0] == 'open')
async def open_dict(callback: types.CallbackQuery): 
    await callback.message.delete()
    await In_dictionary.start.set()
    state = dp.get_current().current_state()
    print(callback.data)
    dictionary = find_dict(callback.data.split('_')[-1])
    await state.update_data(dictionary = dictionary.get_as_dict())
    
    data = await state.get_data()
    print(str(data))

    words_count = len([word.origin for word in dictionary.words])
    await callback.message.answer(f'Ви відкрили словник.\
        \nНазва: "{dictionary.title}"    \
        \nОсновна мова: {dictionary.language_src}  \
        \nМова перекладу: {dictionary.language_dist} \
        \nКількість слів: {words_count}')
    await callback.message.answer('Тепер можете перкладати любі слова і зберігати до вашого словнику', reply_markup=dict_contr_ikb)
    

@dp.message_handler(state=In_dictionary.start, commands='menu')
async def show_menu(message:types.Message):
    await message.answer(text='Выдкриваю меню', reply_markup=dict_contr_ikb)

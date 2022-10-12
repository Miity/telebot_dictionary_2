from copy import deepcopy
import json
from aiogram import types
from loader import dp, bot
from aiogram.dispatcher.storage import FSMContext
from states.states import Create_dictionary
from keyboards.inline.keyboards import choose_lang_ikb,start_ikb
from data.database.commands import add_dict, find_or_new_user, show_dicts


@dp.callback_query_handler(lambda callback: callback.data=='create_dict')
async def create_dict(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(None)
    await Create_dictionary.title.set()
    await callback.message.answer('Введи назву для словника')


@dp.message_handler(state=Create_dictionary.title)
async def dict_title(message: types.Message, state: FSMContext):
    await state.update_data(title = message.text)
    await message.answer("Назва збережена. Тепер вибери мову з якої будемо перекладати", reply_markup=choose_lang_ikb)
    await Create_dictionary.source_lang.set()



@dp.callback_query_handler(state=Create_dictionary.source_lang)
async def choose_source_lang(callback: types.CallbackQuery, state:FSMContext):
    #видалити клавіатуру
    await bot.edit_message_reply_markup(
        callback.from_user.id,
        callback.message.message_id,
        reply_markup=None,
    )
    await state.update_data(src = callback.data) 
    
    await callback.message.answer('Добре, тепер вибери мову на яку будемо перекладать', reply_markup=choose_lang_ikb)
    await Create_dictionary.dist.set()


@dp.callback_query_handler(state=Create_dictionary.dist)
async def choose_lang_dist(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(None)
    await state.update_data(dist = callback.data)

    data = await state.get_data()
    add_dict(callback.from_user.id, data['title'], data['dist'], data['src'])

    user, found =  find_or_new_user(callback.from_user.id)
    start_ikb_dicts = deepcopy(start_ikb)
    dicts =  show_dicts(user)
    for dictionary in dicts:
        start_ikb_dicts.add(types.InlineKeyboardButton(dictionary.title, 
                            callback_data='open_dict_{}'.format(str(dictionary.id))))

    await callback.message.answer('Вітаю, ти створив словарик')
    await callback.message.answer('Відкриємо словарик, чи створемо новий?', reply_markup=start_ikb_dicts)
    await state.finish()

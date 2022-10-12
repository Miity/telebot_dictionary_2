from email import message
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.inline.keyboards import gen_words_ikb, word_edit_ikb
from states.states import In_dictionary
import json


@dp.callback_query_handler(text='delete_dict', state=In_dictionary.start)
@dp.callback_query_handler(text='change_title', state=In_dictionary.start)
@dp.callback_query_handler(text='edit_translate', state=In_dictionary.start)
@dp.callback_query_handler(text='delete', state=In_dictionary.start)
async def start_edit_word(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Функція ще не готова')
    await callback.message.delete()




@dp.callback_query_handler(text='show_words', state=In_dictionary.start)
async def show_words(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    word_origin_arr = [text['origin'] for text in data['dictionary']['words']]
    word_translate_arr = [text['translate'] for text in data['dictionary']['words']]

    text_arr = ['\n{} --> {}\n'.format(x,y).upper() for x,y in zip(word_origin_arr, word_translate_arr)]
    callback_data_arr = ['edit_word_index_{}'.format(str(index)) for index in range(0,len(data['dictionary']['words']))]

    if len(data['dictionary']['words']) > 0:
        ikb = gen_words_ikb(text_arr, callback_data_arr)
        await callback.message.edit_reply_markup(ikb)
        await callback.message.answer('Виберіть слово, щоб відредактувати.\n\n\
        Або продовжіть перекладати слова.')
    else:
        await callback.message.answer('В словарі ще нама слів')


@dp.callback_query_handler(text='edit_dict', state=In_dictionary.start)
async def rdit_dict(callback: types.CallbackQuery):
    from keyboards.inline.keyboards import dict_set_ikb
    await callback.message.answer('Параметри', reply_markup=dict_set_ikb)
    await callback.answer('Параметри')


@dp.callback_query_handler(lambda callback: callback.data.split('_')[0] == 'edit', state=In_dictionary.start)
async def start_edit_word(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    words = data['dictionary']['words']
    word_index = callback.data.split('_')[-1]
    await callback.message.answer('{} --> {}'.format(words[int(word_index)]['origin'],words[int(word_index)]['translate']), reply_markup = word_edit_ikb)

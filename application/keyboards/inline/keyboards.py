from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


add = InlineKeyboardButton('add word', callback_data='add_word')
edit = InlineKeyboardButton('edit translate', callback_data='edit_translate')

keyboard = InlineKeyboardMarkup()
keyboard.add(add, edit)


start_ikb = InlineKeyboardMarkup()
start_ikb.add(InlineKeyboardButton('create dictionary', callback_data='create_dict'))


uk = InlineKeyboardButton('Ukraine', callback_data='uk')
en = InlineKeyboardButton('English', callback_data='en')
it = InlineKeyboardButton('Italian', callback_data='it')

choose_lang_ikb =  InlineKeyboardMarkup()
choose_lang_ikb.add(en,it).add(uk)


dict_contr_ikb = InlineKeyboardMarkup()
show_words_but = InlineKeyboardButton('show words', callback_data='show_words')
edit_dict_but = InlineKeyboardButton('settings',callback_data='edit_dict')
dict_contr_ikb.add(show_words_but)
dict_contr_ikb.add(edit_dict_but)

dict_set_ikb = InlineKeyboardMarkup()
edit_title_but = InlineKeyboardButton('змінити назву', callback_data='change_title')
delete_but = InlineKeyboardButton('видалити словник',callback_data='delete_dict')
dict_set_ikb.add(edit_title_but)
dict_set_ikb.add(delete_but)


def gen_words_ikb(text_arr: list[str], callback_data_arr: list[str]) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    for t, c in zip(text_arr, callback_data_arr):
        but = InlineKeyboardButton(text = t, callback_data=c)
        ikb.add(but)
    return ikb


word_edit_ikb = InlineKeyboardMarkup()
edit_translate_but = InlineKeyboardButton(text='змінити переклад', callback_data='edit_translate')
delete_but_but = InlineKeyboardButton('видалити', callback_data='delete')
word_edit_ikb.add(edit_translate_but,delete_but_but)
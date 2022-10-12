from ast import Str
from .base import session
from .schemas.user import User
from .schemas.dictionary import Dictionary, Word
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import json

# User
def find_or_new_user(telegram_id: int) -> User | bool:
    with session() as sess:
        try:
            stmt =  select(User).where(User.telegram_id.is_(telegram_id))
            user =  sess.scalars(stmt).one()
            return user, True

        except Exception as err:
            print('Exception: ' + str(err))
            user = User(telegram_id = telegram_id)
            sess.add(user)
            sess.commit()
            print('New user id: {}, telegram_id: {}'.format(user.id, user.telegram_id))
            return user, False



# Dictionary
def add_dict(telegram_id: int, title: str, dist: str, src: str) -> Dictionary:
    with session() as sess:
        try:
            dictionary = Dictionary()
            dictionary.title = title
            dictionary.language_dist = dist
            dictionary.language_src = src
            sess.add(dictionary)

            stmt = select(User).where(User.telegram_id.is_(telegram_id))
            user = sess.scalars(stmt).one()
            user.dictionary.append(dictionary)
            
            sess.commit()
            print('New dictionary id:{}, title:{}'.format(dictionary.id,dictionary.title))
            return dictionary
        except Exception as err:
            print('Errore: ', str(err))



def show_dicts(user: User) -> list:
    with session() as sess:
        try:
            stmt = select(Dictionary).where(Dictionary.user_id.is_(user.id))
            dicts = sess.scalars(stmt).all()
            print('Found {} dictionaries'.format(len(dicts)))
            return dicts
        except Exception as err:
            print('Errore: ', str(err))


def find_dict(dict_id) -> Dictionary:
    with session() as sess:
        try:
            stmt = select(Dictionary).where(Dictionary.id.is_(dict_id)).options(selectinload(Dictionary.words))
            dictionary = sess.scalars(stmt).one()
            return dictionary
        except Exception as err:
            print('Errore: ', str(err))


def add_word_to_dict(dict_id: int, origin: str, translate:str) -> None:
    with session() as sess:
        try:
            word = Word()
            word.origin = origin
            word.dict_id = dict_id
            word.translate = translate
            sess.add(word)
            sess.commit()
        except Exception as err:
            print('Errore: ', str(err))

def words_from_dict(dict_id: int) -> list[str]:
    with session() as sess:
        try:
            dictionary = find_dict(dict_id)
            words = dictionary.words
            json_words = {'word':[]}
            for word in words:
                json_words['word'].append({'id':word.id, })
            
            return words
        except Exception as err:
            print('Errore: ', str(err))



# Word

def add_word(text) -> Word:
    with session() as sess:
        try:
            word = Word(origin = text)
            return word
        except Exception as err:
            print('Errore: ', str(err))





###########
def sess():
    with session() as sess:
        try:
            pass
        except Exception as err:
            print('Errore: ', str(err))
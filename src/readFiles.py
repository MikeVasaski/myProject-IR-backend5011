import json
import pickle
import re
import string

import numpy as np
import pandas as pd

from src.bm25 import BM25
from sklearn.feature_extraction.text import TfidfVectorizer

genre_names = [
    'Action', 'Adventure','Comedy', 'Drama','Sci-Fi',
    'Game', 'Space', 'Music', 'Mystery', 'School', 'Fantasy',
    'Horror', 'Kids', 'Sports', 'Magic', 'Romance',]


def genre_to_category(df):
    '''Add genre cagegory column'''
    d = {name :[] for name in genre_names}

    def f(row):
        genres = row.Genres.split(',')
        for genre in genre_names:
            if genre in genres:
                d[genre].append(1)
            else:
                d[genre].append(0)

    # create genre category dict
    df.apply(f, axis=1)
    # add genre category
    genre_df = pd.DataFrame(d, columns=genre_names)
    df = pd.concat([df, genre_df], axis=1)
    return df


def create_text_spelling_check():
    spell = pickle.load(open('../resources/spell_corr_title.pkl', 'rb'))
    spell_s = pickle.load(open('../resources/spell_corr_synopsis.pkl', 'rb'))
    spell = spell + ' ' + spell_s
    spell = spell.to_string()
    spell = re.sub(r'[^\w\s]', '', spell)
    spell = re.sub(r'\n', '', spell)
    pickle.dump(spell, open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/spelling_check.pkl', 'wb'))


def clean_json_data():
    json_f = pd.read_json('D:/3rd-2nd/IR-project/emb_files/anime.json')
    score_df = pd.read_csv('D:/3rd-2nd/IR-953481/py-code/module0/resource/anime.csv')
    rating = pd.read_csv('D:/3rd-2nd/IR-953481/py-code/module0/resource/anime_rating_1000_users.csv')

    first_hd = json_f['images'].apply(lambda x: x['jpg'])
    # print(first_hd)
    img_url_hd = first_hd.apply(lambda x: x['image_url'])
    # print(img_url_hd)
    json_f['images'] = img_url_hd
    # print(json_f['images'])
    trailer_url = json_f['trailer'].apply(lambda x: x['url'])
    json_f['trailer'] = trailer_url
    stu_name = json_f['studios'].apply(lambda x: [i['name'] for i in x])
    json_f['studios'] = stu_name
    gen_name = json_f['genres'].apply(lambda x: [i['name'] for i in x])
    json_f['genres'] = gen_name
    cleaned_title = json_f['title'].apply(lambda x: x.lower())
    cleaned_title = cleaned_title.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    json_f['title'] = cleaned_title
    cleaned_synopsis = json_f['synopsis'].apply(lambda x: x.lower() if x is not None else '')
    cleaned_synopsis = cleaned_synopsis.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    json_f['synopsis'] = cleaned_synopsis
    new_feature = ['mal_id', 'images',
                   'title', 'type', 'genres',
                   'score', 'scored_by', 'members',
                   'favorites', 'synopsis', 'studios']
    json_f = json_f[new_feature]
    cleaned = json_f['score']
    cleaned = cleaned.replace(np.NAN, 0)
    json_f['score'] = cleaned
    cleaned = json_f['scored_by']
    cleaned = cleaned.replace(np.NAN, 0)
    json_f['scored_by'] = cleaned

    # json_f.to_csv(r'D:/3rd-2nd/IR-project/myProject-IR-backend/resources/anime.csv', index=None)
    clean_df = json_f.dropna()
    pickle.dump(rating, open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/rating_1000p.pkl', 'wb'))
    pickle.dump(json_f, open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/anime_data.pkl', 'wb'))
    pickle.dump(json_f['title'], open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/spell_corr_title.pkl', 'wb'))
    pickle.dump(json_f['synopsis'], open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/spell_corr_synopsis.pkl', 'wb'))
def title_synopsis_pkl():
    data = pickle.load(open('../resources/anime_data.pkl', 'rb'))
    title = data['title']
    vectorizer = TfidfVectorizer()
    bm25_title = BM25(vectorizer)
    bm25_title.fit(title)
    pickle.dump(bm25_title, open('../resources/ani_title.pkl', 'wb'))

    synopsis = data['synopsis']
    synopsis = synopsis.dropna()
    bm25_syno = BM25(vectorizer)
    bm25_syno.fit(synopsis)
    pickle.dump(bm25_syno, open('../resources/ani_synopsis.pkl', 'wb'))

    # rating = pickle.dump(data['score'], open('../resources/rate.pkl', 'wb'))


# if __name__ == '__main__':
#     clean_json_data()
#     title_synopsis_pkl()
#     create_text_spelling_check()
#     print('cleaned data are all done!')
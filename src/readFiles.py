import json
import pickle
import string

import numpy as np
import pandas as pd

from src.bm25 import BM25
from sklearn.feature_extraction.text import TfidfVectorizer


# def create_anime_dat_pkl():
#     data = pd.read_csv('../resources/anime.csv')
#     cleaned_title = pd.Series(data['title'])
#     cleaned_title = cleaned_title.apply(lambda s: s.lower())
#     cleaned_title = cleaned_title.apply(lambda s: s.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
#     data['title'] = cleaned_title
#     cleaned_desc = pd.Series(data['synopsis'])
#     cleaned_desc = cleaned_desc.str.lower()
#     data['synopsis'] = cleaned_desc
#     pickle.dump(data, open('../resources/anime_data.pkl', 'wb'))
#     print("anime_data.pkl is created!")


def clean_json_data():
    json_f = pd.read_json('D:/3rd-2nd/IR-project/emb_files/anime.json')
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
    json_f['title'] = cleaned_title
    cleaned_synopsis = json_f['synopsis'].apply(lambda x: x.lower() if x is not None else '')
    cleaned_synopsis = cleaned_synopsis.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    json_f['synopsis'] = cleaned_synopsis
    new_feature = ['mal_id', 'url', 'images',
                   'title', 'type', 'genres',
                   'score', 'synopsis', 'studios']
    json_f = json_f[new_feature]
    clean_df = json_f.dropna()
    pickle.dump(clean_df, open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/anime_data.pkl', 'wb'))




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

if __name__ == '__main__':
    clean_json_data()
    title_synopsis_pkl()
    print('cleaned data are all done!')
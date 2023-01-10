import json
import pickle
import string

import numpy as np
import pandas as pd

from src.bm25 import BM25
from nltk import PorterStemmer, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


def preProcess(s):
    ps = PorterStemmer()
    s = word_tokenize(s)
    stopwords_set = set(stopwords.words())
    s = [w for w in s if w not in stopwords_set]
    # s = [w for w in s if not w.isdigit()]
    s = [ps.stem(w) for w in s]
    s = ' '.join(s)
    return s


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


def secret_jutsu():
    json_f = pd.read_json('D:/3rd-2nd/IR-project/emb_files/anime.json')
    json_f['images'] = json_f['images'].apply(lambda x: x['jpg']['image_url'])
    json_f['studios'] = json_f['studios'].apply(lambda x: [i['name'] for i in x])
    json_f['genres'] = json_f['genres'].apply(lambda x: [i['name'] for i in x])
    json_f['licensors'] = json_f['licensors'].apply(lambda x: [i['name'] for i in x])
    json_f['producers'] = json_f['producers'].apply(lambda x: [i['name'] for i in x])
    json_f['demographics'] = json_f['demographics'].apply(lambda x: [i['name'] for i in x])
    json_f.drop(columns=['trailer', 'approved', 'titles', 'title_english', 'title_japanese',
                         'title_synonyms', 'airing', 'aired', 'broadcast', 'explicit_genres',
                         'themes'], inplace=True)

    cleaned_title = json_f['title']
    cleaned_title = cleaned_title.apply(lambda x: x.lower())
    cleaned_title = cleaned_title.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    json_f['title'] = cleaned_title

    cleaned_synopsis = json_f['synopsis']
    cleaned_synopsis = cleaned_synopsis.apply(lambda x: x.lower() if x is not None else '')
    cleaned_synopsis = cleaned_synopsis.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    json_f['synopsis'] = cleaned_synopsis

    # files = pd.read_json('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/anime.json')
    # json_f.to_csv(r'D:/3rd-2nd/IR-project/emb_files/anime.csv', index=None)
    pickle.dump(json_f, open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/anime_data.pkl', 'wb'))
    # print('anime_data was dumped!')


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

    title_data = pickle.load(open('../resources/ani_title.pkl', 'rb'))
    query = "naruto"
    result = title_data.transform(query)
    rank = np.argsort(result)[::-1]
    print(data.iloc[rank[:10]].to_markdown())


def get_anime_data():
    data = pickle.load(open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/anime_data.pkl', 'rb'))
    return data
# if __name__ == '__main__':
#     title_synopsis_pkl()

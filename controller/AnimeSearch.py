import pickle

import pandas as pd

anime = pickle.load(open('../resources/anime_data.pkl', 'rb'))
title = pickle.load(open('../resources/ani_title.pkl', 'rb'))
synopsis = pickle.load(open('../resources/ani_synopsis.pkl', 'rb'))


def query_scoring(query):
    score_t = title.transform(query)
    score_s = synopsis.transform(query)
    sum_score = score_t + score_s
    tf = pd.DataFrame({'bm25-score': list(sum_score),
                       'mal_id': list(anime['mal_id']),
                       'title': list(anime['title']),
                       'type': list(anime['type']),
                       'genres': list(anime['genres']),
                       'score': list(anime['score']),
                       'synopsis': list(anime['synopsis']),
                       'studios': list(anime['studios']),
                       'image': list(anime['image']),
                       'url': list(anime['url'])
                       }).nlargest(columns='bm25-score', n=20)
    tf['rank'] = tf['bm25'].rank(ascending=False)
    tf = tf.drop(columns='bm25', axis=1)
    tf = tf.to_dict('record')
    return tf

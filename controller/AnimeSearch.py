import json
import pickle
from src.LTR import predict, make_user_feature
import pandas as pd

anime = pickle.load(open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/anime_data.pkl', 'rb'))
title = pickle.load(open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/ani_title.pkl', 'rb'))
synopsis = pickle.load(open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/ani_synopsis.pkl', 'rb'))
rating = pickle.load(open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/rating_1000p.pkl', 'rb'))


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
                       'favorites': list(anime['favorites']),
                       'synopsis': list(anime['synopsis']),
                       'studios': list(anime['studios']),
                       'image': list(anime['images']),
                       'url': list(anime['url'])
                       }).nlargest(columns='bm25-score', n=20)
    tf['rank'] = tf['bm25-score'].rank(ascending=False)
    tf = tf.drop(columns='bm25-score', axis=1)
    tf = tf.to_dict('record')
    return tf


def get_ani_list():
    # user_id = 14
    # user_df = rating.copy().loc[rating['user_id'] == user_id]
    # user_df = make_user_feature(user_df)
    # anime_rec = predict(user_df, 10, anime, rating)
    bound = len(anime)
    tf = pd.DataFrame({'mal_id': list(anime['mal_id']),
                       'title': list(anime['title']),
                       'type': list(anime['type']),
                       'genres': list(anime['genres']),
                       'score': list(anime['score']),
                       'favorites': list(anime['favorites']),
                       'synopsis': list(anime['synopsis']),
                       'studios': list(anime['studios']),
                       'image': list(anime['images']),
                       'url': list(anime['url'])
                       }).nlargest(columns='mal_id', n=bound)
    tf = tf.to_dict('record')
    return tf


def list_bookmark(book):
    res = []
    score = []
    for i in book:
        temp = anime[anime['mal_id'] == i['ani_id']].to_dict('records')[0]
        # score.append(temp['score'])
        res.append(temp)
    res.sort(key=lambda i: i['score'], reverse=True)
    # print(res)
    # print(score)
    # score.sort(reverse=True)
    # print("after sorting")
    # print(score)

    # ranking
    return res
import pickle
import numpy as np

from flask import request
from src.readFiles import get_anime_data


class AnimeSearch:

    @staticmethod
    def search_by_title():
        data = get_anime_data()
        title = pickle.load(open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/ani_title.pkl', 'rb'))
        query = request.get_json()['search']
        result = title.transform(query)
        rank = np.argsort(result)[::-1]
        list_title = data['title'].iloc[rank[:20]].to_json()
        return list_title

    @staticmethod
    def search_by_synopsis():
        data = get_anime_data()
        synopsis = pickle.load(open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/ani_synopsis.pkl', 'rb'))
        query = request.get_json()['search']
        result = synopsis.transform(query)
        rank = np.argsort(result)[::-1]
        list_synopsis = data['synopsis'].iloc[rank[:20]].to_json()
        return list_synopsis

    @staticmethod
    def default():
        data = get_anime_data()
        all_data = data.to_json()
        return all_data
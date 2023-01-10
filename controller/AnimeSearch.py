import pickle
import numpy as np
import pandas as pd

from flask import request, jsonify
from src.readFiles import get_anime_data


class AnimeSearch:

    @staticmethod
    def search_by_title():
        # data = get_anime_data()
        # df_data = pd.DataFrame(data=data)
        # title = pickle.load(open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/ani_title.pkl', 'rb'))
        # query = request.get_json()['search']
        # result = title.transform(query)
        # df_data['bm25'] = list(result)
        # df_data['rank'] = df_data['bm25'].rank(ascending=False)
        # df_data = df_data.nlargest(columns='bm25', n=20)
        # df_data = df_data.drop(columns='bm25', axis=1)
        # # df_data['score'] =
        # json_data = jsonify({'info': df_data.to_dict('records')}), 200
        #
        # # rank = np.argsort(result)[::-1]
        # # list_title = data.iloc[rank[:20]].to_dict('records')
        return None

    # @staticmethod
    # def search_by_synopsis():
    #     data = get_anime_data()
    #     df_data = pd.DataFrame(data=data)
    #     synopsis = pickle.load(open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/ani_synopsis.pkl', 'rb'))
    #     query = request.get_json()['search']
    #     result = synopsis.transform(query)
    #     df_data['bm25'] = list(result)
    #     df_data['rank'] = df_data['bm25'].rank(ascending=False)
    #     df_data = df_data.nlargest(columns='bm25', n=20)
    #     df_data = df_data.drop(columns='bm25', axis=1)
    #     json_data = jsonify({'info': df_data.to_dict('records')}), 200
    #     # rank = np.argsort(result)[::-1]
    #     # list_synopsis = data.iloc[rank[:20]].to_dict()
    #     return json_data

    @staticmethod
    def default():
        data = get_anime_data()
        all_data = data.to_dict()
        return all_data
import string

import pandas as pd
from spellchecker import SpellChecker
from flask import Flask, request, make_response, jsonify
from sqlalchemy_utils.functions import database_exists, create_database
from controller.AnimeSearch import query_scoring, get_ani_list, anime, title, synopsis
from controller.userController import UserController
from model.bookmark import BookmarkSchema, Bookmark
from model.database import db
from flask_cors import CORS, cross_origin

from src.LTR import make_user_feature, predict

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1:3306/ir_pj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])

db.init_app(app)

with app.app_context():
    db.create_all()

bookmark_schema = BookmarkSchema()
bookmarks_schema = BookmarkSchema(many=True)

spell = SpellChecker()
spell.word_frequency.load_text('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/spelling_check.pkl')


def check_spell(query):
    spell_correctness = [spell.correction(w) for w in query.split()]
    cor_word = spell_correctness[0]
    return cor_word, query


@app.route('/login', methods=['POST'])
def user_login():
    return UserController.login()


@app.route('/search', methods=['POST'])
def add_favorite():
    query = request.get_json()['search']
    query = query.lower().translate(str.maketrans('', '', string.punctuation))
    corr_word, query = check_spell(query)
    if (corr_word != query):
        print(query)
        print("Did you mean: " + corr_word + " ?")
    res = query_scoring(corr_word)
    res = {'result': res, 'correction': corr_word, 'query': query}
    return make_response(jsonify(res), 200)


@app.route('/')
def get_all_anime():
    res = get_ani_list()
    res = {'result': res}
    return make_response(jsonify(res), 200)


@app.route('/addBookmark', methods=['POST'])
@cross_origin()
def add_bookmark():
    uid = request.get_json()['uid']
    ani_id = request.get_json()['mal_id']
    score = request.get_json()['score']
    res = Bookmark(uid, ani_id, score)
    # print(res)
    db.session.add(res)
    db.session.commit()
    return bookmark_schema.jsonify(res), 200


@app.route('/Bookmark', methods=['DELETE'])
def remove_bookmark():
    uid = request.get_json()['uid']
    ani_id = request.get_json()['mal_id']
    # bmD = Bookmark.query.get(uid=uid, ani_id=ani_id)
    # print(bmD)
    # res = db.session.execute(db.select(Bookmark)).filter_by(uid=uid, ani_id=ani_id).first()
    res = db.session.query(Bookmark).filter_by(uid=uid, ani_id=ani_id).first()
    # print(res)
    db.session.delete(res)
    db.session.commit()
    return jsonify('delete'), 200


@app.route('/Bookmark', methods=['GET'])
def get_bookmark():
    uid = request.get_json()['uid']
    res = []
    all_book = db.session.query(Bookmark).filter_by(uid=uid).all()
    all_book = Bookmark.serialize_list(all_book)
    for i in all_book:
        temp = anime[anime['mal_id'] == i['ani_id']].to_dict('records')[0]
        res.append(temp)
    res.sort(key=lambda i: i['score'], reverse=True)
    return jsonify({'result': res}), 200


# @app.route('/suggestion', methods=['POST'])
# def suggestion():
#     uid = request.get_json()['uid']
#     # prepare to compare
#     book_ser = db.session.query(Bookmark).filter_by(uid=uid).all()
#     book_ser = Bookmark.serialize_list(book_ser)
#     book_df = pd.DataFrame(book_ser)
#     book_df = book_df.drop(columns='id')
#     print(book_df)
#     print(book_df['uid'])
#     user_df = pd.DataFrame(book_df)
#     print(user_df)
#     user_df = make_user_feature(user_df)
#     print(user_df)
#     res = predict(user_df, 10, anime, book_df)
#     # print(res)
#     # user_df = book_ser.copy().loc[]
#     # for i in book_ser:
#     #     temp = anime[anime['mal_id'] == i['ani_id']].to_dict('records')[0]
#     #
#     # df = pd.DataFrame()
#     return jsonify({'result': res}), 200


@app.route('/animeDetails/<id>?', methods=['GET'])
def post_details(id):
    ani_detail = Bookmark.quey.get(id)
    return bookmark_schema.jsonify(ani_detail)


if __name__ == '__main__':
    app.run(debug=True)
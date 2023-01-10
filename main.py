import pickle
import string
from spellchecker import SpellChecker
from flask import Flask, request, make_response, jsonify
from sqlalchemy_utils.functions import database_exists, create_database
from controller.AnimeSearch import query_scoring
from controller.userController import UserController
from model.database import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1:3306/ir_pj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])

db.init_app(app)

with app.app_context():
    db.create_all()

anime = pickle.load(open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/anime_data.pkl', 'rb'))
title = pickle.load(open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/ani_title.pkl', 'rb'))
synopsis = pickle.load(open('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/ani_synopsis.pkl', 'rb'))

spell = SpellChecker()
spell.word_frequency.load_text('D:/3rd-2nd/IR-project/myProject-IR-backend/resources/spelling_check.pkl')


def check_spell(query):
    spell_correctness = [spell.correction(w) for w in query.split()]
    cor_word = spell_correctness[0]
    return cor_word


@app.route('/login', methods=['POST'])
def user_login():
    return UserController.login()


@app.route('/search', methods=['POST'])
def add_favorite():
    query = request.get_json()['search']
    query = query.lower().translate(str.maketrans('', '', string.punctuation))
    query = check_spell(query)
    res = query_scoring(query)
    res = {'result': res, 'correction': query}
    return make_response(jsonify(res), 200)

# @app.route('/', methods=['GET'])
# def default():
#     return AnimeSearch.default()


if __name__ == '__main__':
    app.run(debug=True)
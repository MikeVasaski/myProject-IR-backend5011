import string
from spellchecker import SpellChecker
from flask import Flask, request, make_response, jsonify
from sqlalchemy_utils.functions import database_exists, create_database
from controller.AnimeSearch import query_scoring, get_ani_list
from controller.userController import UserController
from model.bookmark import BookmarkSchema, Bookmark
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
def add_bookmark():
    uid = request.get_json()['uid']
    ani_id = request.get_json()['mal_id']
    res = Bookmark(uid, ani_id)
    print(res)
    db.session.add(res)
    db.session.commit()
    return bookmark_schema.jsonify(res), 200


if __name__ == '__main__':
    app.run(debug=True)
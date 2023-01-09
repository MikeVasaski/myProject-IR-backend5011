from flask import Flask
from sqlalchemy_utils.functions import database_exists, create_database
from controller.AnimeSearch import AnimeSearch
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


@app.route('/login', methods=['POST'])
def user_login():
    return UserController.login()


@app.route('/searchByTitle', methods=['POST'])
def search_by_title():
    return AnimeSearch.search_by_title()


@app.route('/searchBySynopsis', methods=['POST'])
def search_by_synopsis():
    return AnimeSearch.search_by_synopsis()


if __name__ == '__main__':
    app.run(debug=True)
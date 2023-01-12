import bcrypt
import jwt
from flask import jsonify, request
import datetime
from .database import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    favorite = db.Column(db.Integer, nullable=True)
    bookmark = db.Column(db.Integer, nullable=True)

    def __init__(self, username, password, email, bookmark,favorite):
        self.username = username
        self.email = email
        self.password = password
        self.bookmark = bookmark
        self.favorite = favorite

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'bookmark': self.bookmark,
            'favorite': self.favorite
        }

    @staticmethod
    def login():
        try:
            username = request.get_json()['username']
            password = request.get_json()['password']
            try:
                user = User.query.filter_by(username=username).first()
                if bcrypt.checkpw(password.encode('utf-8'), bytes(user.password, 'utf-8')):
                    user_serialize = user.serialize
                    token = jwt.encode(
                        {'user': user_serialize, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)},
                        'Bearer')
                    return jsonify({'user': user_serialize, 'token': token}), 200
                raise
            except:
                return jsonify({'message': 'username or password is incorrect'}), 401
        except:
            return jsonify({'message': 'The request body required username, password'}), 400
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

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = password

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
        }